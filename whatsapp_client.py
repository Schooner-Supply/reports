"""
whatsapp_client.py — WhatsApp-ilmoitukset päiväraporteista (Cloud API)

Lähettää tiivistetyn ilmoituksen Schoonerin WhatsApp Business -numerosta
annetuille vastaanottajille, kun raportin status on yellow tai red.
Green-raportit ovat hiljaisia oletuksena, kuten Slackissa.

Konfiguraatio (ympäristömuuttujat / GitHub Actions -secretit):
  WHATSAPP_ACCESS_TOKEN      System User -token (whatsapp_business_messaging)
  WHATSAPP_PHONE_NUMBER_ID   Yritysnumeron Phone Number ID (ei itse numero)
  WHATSAPP_ALERT_RECIPIENTS  Vastaanottajat pilkuilla, E.164: +358401234567,+358…
  WHATSAPP_REPORT_TEMPLATE   Hyväksytyn viestipohjan nimi (ks. alla)
  WHATSAPP_TEMPLATE_LANG     Pohjan kielikoodi, oletus fi
  WHATSAPP_NOTIFY_GREEN      "true" jos haluat ilmoituksen myös vihreistä
  WHATSAPP_GRAPH_VERSION     oletus v21.0

Miksi viestipohja: WhatsAppissa yritys saa lähettää vapaata tekstiä vain
24 tunnin sisällä vastaanottajan viimeisestä viestistä. Aamuraportti on
yrityksen aloittama viesti, joten se vaatii Metan hyväksymän pohjan
(Meta Business Suite → WhatsApp Manager → Message templates, kategoria
UTILITY). Pohjan rungossa on neljä paikkaa:

    {{1}} päivä, esim. "Ti 21.10.2026"
    {{2}} status, esim. "🔴 Toimenpiteitä"
    {{3}} yhteenveto (1–3 riviä yhdessä)
    {{4}} ClickUp-linkki tai "-"

Esimerkkipohja (nimi shopify_daily_report):
    Shopify-päiväraportti {{1}} — {{2}}
    {{3}}
    Raportti: {{4}}

Jos pohjaa ei ole asetettu, yritetään vapaata tekstiä. Se onnistuu vain
jos vastaanottaja on kirjoittanut numeroon viimeisen vuorokauden sisällä;
muuten Meta palauttaa virheen 131047 ja ilmoitus jää lähettämättä
(lokiin, ei kaadu).
"""

import logging
import os
import re
from datetime import date
from typing import Optional

import requests

log = logging.getLogger(__name__)

STATUS_EMOJI = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
STATUS_LABEL = {"green": "Normaali", "yellow": "Huomioitavaa", "red": "Toimenpiteitä"}

# Metan virhekoodi: 24 h ikkuna kiinni, tarvitaan viestipohja.
ERR_REENGAGEMENT = 131047
# Cloud API:n tekstiviestin ja pohjaparametrin rajat.
TEXT_MAX = 4096
PARAM_MAX = 1024


def send_report_notification(
    report_date: date,
    status_level: str,
    summary_lines: list[str],
    recommendation: str,
    clickup_url: Optional[str] = None,
    alerts_count: int = 0,
) -> bool:
    """Lähettää WhatsApp-ilmoituksen päiväraportista kaikille vastaanottajille.

    Lähettää aina red/yellow-statuksella.
    Green lähetetään vain jos WHATSAPP_NOTIFY_GREEN=true.

    Palauttaa True jos vähintään yksi lähetys onnistui.
    """
    token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    recipients = parse_recipients(os.getenv("WHATSAPP_ALERT_RECIPIENTS", ""))
    if not token or not phone_number_id or not recipients:
        log.debug("WhatsApp ei konfiguroitu (token, phone_number_id tai vastaanottajat puuttuu) — ohitetaan")
        return False

    notify_green = os.getenv("WHATSAPP_NOTIFY_GREEN", "false").lower() == "true"
    if status_level == "green" and not notify_green:
        log.debug("Green-raportti — ei WhatsApp-ilmoitusta (WHATSAPP_NOTIFY_GREEN=false)")
        return False

    template = os.getenv("WHATSAPP_REPORT_TEMPLATE", "").strip()
    lang = os.getenv("WHATSAPP_TEMPLATE_LANG", "fi").strip() or "fi"
    graph_version = os.getenv("WHATSAPP_GRAPH_VERSION", "v21.0")
    url = f"https://graph.facebook.com/{graph_version}/{phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    ok_any = False
    for to in recipients:
        if template:
            payload = build_template_payload(
                to, template, lang,
                template_params(report_date, status_level, summary_lines, recommendation, clickup_url, alerts_count),
            )
        else:
            payload = build_text_payload(
                to, build_text(report_date, status_level, summary_lines, recommendation, clickup_url, alerts_count),
            )
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            if resp.ok:
                log.info(f"WhatsApp-ilmoitus lähetetty {to} (status={status_level}, {'pohja ' + template if template else 'teksti'})")
                ok_any = True
                continue
            code = _error_code(resp)
            if code == ERR_REENGAGEMENT:
                log.warning(
                    f"WhatsApp {to}: 24 h ikkuna kiinni eikä viestipohjaa ole asetettu "
                    "(WHATSAPP_REPORT_TEMPLATE). Ilmoitus jäi lähettämättä."
                )
            else:
                log.warning(f"WhatsApp-ilmoitus epäonnistui {to}: HTTP {resp.status_code} {resp.text[:300]}")
        except requests.RequestException as e:
            log.warning(f"WhatsApp-ilmoitus epäonnistui {to}: {e}")
    return ok_any


# ── Puhdas logiikka (testattavissa ilman verkkoa) ─────────────────────────────

def parse_recipients(csv: str) -> list[str]:
    """"+358 40 123 4567, 040 7654321" -> ["358401234567", "358407654321"]."""
    out: list[str] = []
    for part in (csv or "").split(","):
        wa = to_wa_id(part)
        if wa and wa not in out:
            out.append(wa)
    return out


def to_wa_id(phone: str, default_country: str = "358") -> str:
    """Mikä tahansa kirjoitusasu -> pelkät numerot maakoodilla (wa_id)."""
    s = re.sub(r"[^\d+]", "", (phone or "").strip())
    if s.startswith("00"):
        s = "+" + s[2:]
    if s.startswith("+"):
        return re.sub(r"\D", "", s[1:])
    s = re.sub(r"\D", "", s)
    if s.startswith("0"):
        return default_country + s[1:]
    return s


def format_date(report_date: date) -> str:
    weekdays = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    return f"{weekdays[report_date.weekday()]} {report_date.day}.{report_date.month}.{report_date.year}"


def _status_text(status_level: str) -> str:
    return f"{STATUS_EMOJI.get(status_level, '⚪')} {STATUS_LABEL.get(status_level, status_level)}".strip()


def _one_line(s: str, limit: int) -> str:
    """Pohjaparametri ei saa sisältää rivinvaihtoja, tabulaattoreita eikä yli
    neljää peräkkäistä välilyöntiä (Meta hylkää). Tiivistetään yhdelle riville."""
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"


def template_params(
    report_date: date,
    status_level: str,
    summary_lines: list[str],
    recommendation: str,
    clickup_url: Optional[str],
    alerts_count: int,
) -> list[str]:
    """Pohjan {{1}}–{{4}}: päivä, status, yhteenveto, linkki."""
    summary = " · ".join(line.strip() for line in summary_lines[:3] if line.strip()) or "Ei tilauksia."
    if alerts_count > 0:
        summary += f" · ⚠️ {alerts_count} alerttia"
    if recommendation:
        summary += f" · Suositus: {recommendation}"
    return [
        _one_line(format_date(report_date), 60),
        _one_line(_status_text(status_level), 40),
        _one_line(summary, PARAM_MAX),
        _one_line(clickup_url or "-", 500),
    ]


def build_text(
    report_date: date,
    status_level: str,
    summary_lines: list[str],
    recommendation: str,
    clickup_url: Optional[str],
    alerts_count: int,
) -> str:
    """Vapaamuotoinen viesti (vain 24 h ikkunan sisällä)."""
    lines = [f"*Shopify-päiväraportti {format_date(report_date)}* — {_status_text(status_level)}", ""]
    lines += [f"- {line}" for line in summary_lines[:4]] or ["Ei tilauksia."]
    if alerts_count > 0:
        lines += ["", f"⚠️ Alertteja: {alerts_count} kpl"]
    if recommendation:
        lines += ["", f"*Suositus:* {recommendation}"]
    if clickup_url:
        lines += ["", f"Raportti: {clickup_url}"]
    text = "\n".join(lines)
    return text if len(text) <= TEXT_MAX else text[: TEXT_MAX - 1] + "…"


def build_text_payload(to: str, body: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_wa_id(to),
        "type": "text",
        "text": {"preview_url": False, "body": body[:TEXT_MAX]},
    }


def build_template_payload(to: str, name: str, lang: str, params: list[str]) -> dict:
    components = []
    if params:
        components.append({
            "type": "body",
            "parameters": [{"type": "text", "text": p[:PARAM_MAX]} for p in params],
        })
    return {
        "messaging_product": "whatsapp",
        "to": to_wa_id(to),
        "type": "template",
        "template": {"name": name, "language": {"code": lang}, "components": components},
    }


def _error_code(resp: requests.Response) -> Optional[int]:
    try:
        code = resp.json().get("error", {}).get("code")
        return int(code) if code is not None else None
    except (ValueError, AttributeError):
        return None

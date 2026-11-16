"""
conversion_guard.py — Poikkeamahälytys Shopifyn omasta sessiodatasta (vartija 3)

Miksi tämä on olemassa (16.11.2026): evästebanneri nappasi kaikki klikkaukset
kortin ulkopuolelta, eikä "Lisää ostoskoriin" lähettänyt mitään. PostHog
käynnistyy vasta suostumuksen jälkeen, joten se ei nähnyt yhtään kävijää,
johon vika osui. Hälytyksen on siis perustuttava Shopifyn omiin lukuihin.

Mitä mitataan (ShopifyQL, sessions-taulu):
  - korilisäyksiä per sessio  (sessions_with_cart_additions / sessions)
  - tilauksia per sessio       (sessions_that_completed_checkout / sessions)
Eilinen verrataan sitä edeltävän seitsemän päivän liukuvaan keskiarvoon.
Pudotus yli 50 % → punainen → WhatsApp-push (sama Cloud API kuin
päiväraportissa). Molemmat suhteet raportoidaan aina lokiin.

Miksi vain Pohjoismaat (Finland, Sweden, Norway, Denmark, Åland Islands):
1.–16.11.2026 kaupan sessioista 3 527 tuli Yhdysvalloista ja 528 Brasiliasta,
0 ja 0 toteutunutta tilausta — skrapperi- ja korttitestausbotteja, jotka
nostivat "kassalle asti" -lukuja satoihin päivässä. Ilman maarajausta botit
sekä peittäisivät oikean pudotuksen että laukaisisivat vääriä hälytyksiä.
Pohjoismaissa tilaukset syntyvät (FI 13, SE 10 samalla jaksolla).

Ympäristömuuttujat: SHOPIFY_SHOP, SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET,
SHOPIFY_API_VERSION (ShopifyQL vaatii sovellukselta read_reports-oikeuden),
WHATSAPP_* kuten whatsapp_client.py:ssä. Valinnaiset:
  GUARD_DROP_THRESHOLD   oletus 0.5  (50 % pudotus)
  GUARD_MIN_SESSIONS     oletus 30   (alle tämän eilisen luku on liian ohut
                                     hälytykseen; raportoidaan keltaisena)
  GUARD_COUNTRIES        oletus "Finland,Sweden,Norway,Denmark,Åland Islands"

Käyttö:  python conversion_guard.py [--date YYYY-MM-DD] [--dry-run]
Paluuarvo 0 = normaali/keltainen, 1 = punainen (hälytys), 3 = dataa ei saatu.
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

import requests

log = logging.getLogger("conversion_guard")

DEFAULT_COUNTRIES = "Finland,Sweden,Norway,Denmark,Åland Islands"


@dataclass
class DayRow:
    day: date
    sessions: int
    cart_sessions: int
    order_sessions: int

    @property
    def cart_rate(self) -> Optional[float]:
        return self.cart_sessions / self.sessions if self.sessions else None

    @property
    def order_rate(self) -> Optional[float]:
        return self.order_sessions / self.sessions if self.sessions else None


@dataclass
class Verdict:
    day: date
    status: str                      # green | yellow | red
    lines: list[str] = field(default_factory=list)
    cart_rate: Optional[float] = None
    cart_ref: Optional[float] = None
    order_rate: Optional[float] = None
    order_ref: Optional[float] = None
    sessions: int = 0
    ref_sessions: int = 0


# ── Puhdas logiikka (testattavissa ilman verkkoa) ─────────────────────────────

def pct_drop(reference: Optional[float], current: Optional[float]) -> Optional[float]:
    """Positiivinen luku = pudotus (0.6 = -60 %). None jos vertailua ei voi tehdä."""
    if reference is None or current is None or reference <= 0:
        return None
    return (reference - current) / reference


def rolling_reference(history: list[DayRow]) -> tuple[Optional[float], Optional[float], int]:
    """Edeltävien päivien yhteenlasketut suhteet (ei päiväkeskiarvojen keskiarvo:
    hiljainen päivä ei saa painaa yhtä paljon kuin vilkas)."""
    s = sum(r.sessions for r in history)
    if s <= 0:
        return None, None, 0
    return (sum(r.cart_sessions for r in history) / s,
            sum(r.order_sessions for r in history) / s, s)


def judge(today: DayRow, history: list[DayRow], threshold: float = 0.5, min_sessions: int = 30) -> Verdict:
    cart_ref, order_ref, ref_sessions = rolling_reference(history)
    v = Verdict(day=today.day, status="green", cart_rate=today.cart_rate, cart_ref=cart_ref,
                order_rate=today.order_rate, order_ref=order_ref, sessions=today.sessions,
                ref_sessions=ref_sessions)

    def fmt(x: Optional[float]) -> str:
        return "–" if x is None else f"{x * 100:.1f} %"

    v.lines.append(f"Sessioita {today.sessions} (7 pv yht. {ref_sessions}).")
    v.lines.append(f"Korilisäyksiä/sessio {fmt(today.cart_rate)} vs 7 pv {fmt(cart_ref)}.")
    v.lines.append(f"Tilauksia/sessio {fmt(today.order_rate)} vs 7 pv {fmt(order_ref)}.")

    if len(history) < 3 or ref_sessions <= 0:
        v.status = "yellow"
        v.lines.append("Vertailudataa alle 3 päivältä — ei hälytystä.")
        return v

    if today.sessions < min_sessions:
        v.status = "yellow"
        v.lines.append(f"Vain {today.sessions} sessiota (< {min_sessions}) — luku liian ohut hälytykseen.")
        return v

    drops = []
    cd = pct_drop(cart_ref, today.cart_rate)
    if cd is not None and cd > threshold:
        drops.append(f"korilisäykset/sessio −{cd * 100:.0f} %")
    od = pct_drop(order_ref, today.order_rate)
    # Tilauksia on vähän: alle 3 tilausta/7 pv ei kanna hälytystä yksinään.
    if od is not None and od > threshold and sum(r.order_sessions for r in history) >= 3:
        drops.append(f"tilaukset/sessio −{od * 100:.0f} %")

    if drops:
        v.status = "red"
        v.lines.insert(0, "PUDOTUS: " + ", ".join(drops) + " (raja 50 %).")
    return v


def parse_shopifyql_rows(table: dict) -> list[DayRow]:
    """ShopifyqlTableData {columns:[{name}], rows:[{...}]} -> DayRow-lista."""
    cols = [c["name"] for c in table.get("columns", [])]
    rows = table.get("rows") or []
    out: list[DayRow] = []
    for r in rows:
        if isinstance(r, list):
            r = dict(zip(cols, r))
        day = str(r.get("day") or r.get("Day") or "")[:10]
        if not day:
            continue
        out.append(DayRow(
            day=date.fromisoformat(day),
            sessions=int(float(r.get("sessions") or 0)),
            cart_sessions=int(float(r.get("sessions_with_cart_additions") or 0)),
            order_sessions=int(float(r.get("sessions_that_completed_checkout") or 0)),
        ))
    out.sort(key=lambda x: x.day)
    return out


def build_query(start: date, end: date, countries: list[str]) -> str:
    quoted = ", ".join("'" + c.replace("'", "''") + "'" for c in countries)
    return (
        "FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_completed_checkout "
        f"WHERE session_country IN ({quoted}) "
        f"TIMESERIES day SINCE {start.isoformat()} UNTIL {end.isoformat()}"
    )


# ── Verkko ─────────────────────────────────────────────────────────────────────

def fetch_rows(start: date, end: date, countries: list[str]) -> list[DayRow]:
    import config
    from shopify_client import _get_access_token

    gql = """query($q: String!) { shopifyqlQuery(query: $q) { tableData { columns { name dataType } rows } parseErrors } }"""
    url = f"https://{config.SHOPIFY_SHOP}/admin/api/{config.SHOPIFY_API_VERSION}/graphql.json"
    resp = requests.post(url, json={"query": gql, "variables": {"q": build_query(start, end, countries)}},
                         headers={"X-Shopify-Access-Token": _get_access_token()}, timeout=60)
    resp.raise_for_status()
    body = resp.json()
    if body.get("errors"):
        # Tyypillisin syy: sovelluksella ei ole read_reports-oikeutta.
        raise RuntimeError(f"ShopifyQL GraphQL-virhe: {json.dumps(body['errors'])[:500]}")
    data = (body.get("data") or {}).get("shopifyqlQuery") or {}
    if data.get("parseErrors"):
        raise RuntimeError(f"ShopifyQL parse: {data['parseErrors']}")
    return parse_shopifyql_rows(data.get("tableData") or {})


def send_push(v: Verdict, run_url: Optional[str]) -> bool:
    from whatsapp_client import send_report_notification
    # Sama hyväksytty pohja kuin päiväraportissa: {{1}} päivä, {{2}} status,
    # {{3}} yhteenveto, {{4}} linkki. Otsikko on pohjassa "Shopify-päiväraportti",
    # mutta sisältö kertoo että kyse on konversiovartijasta.
    lines = ["Konversiovartija: " + v.lines[0]] + v.lines[1:3]
    return send_report_notification(
        report_date=v.day, status_level=v.status, summary_lines=lines,
        recommendation="Tarkista evästebanneri/ostonappi ja Actions-ajo.",
        clickup_url=run_url, alerts_count=1,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="tarkasteltava päivä (oletus eilen, Europe/Helsinki)")
    ap.add_argument("--dry-run", action="store_true", help="ei WhatsApp-lähetystä")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    tz = ZoneInfo(os.getenv("TIMEZONE", "Europe/Helsinki"))
    day = date.fromisoformat(a.date) if a.date else (datetime.now(tz).date() - timedelta(days=1))
    threshold = float(os.getenv("GUARD_DROP_THRESHOLD") or 0.5)
    min_sessions = int(os.getenv("GUARD_MIN_SESSIONS") or 30)
    countries = [c.strip() for c in (os.getenv("GUARD_COUNTRIES") or DEFAULT_COUNTRIES).split(",") if c.strip()]

    try:
        rows = fetch_rows(day - timedelta(days=7), day, countries)
    except Exception as e:  # noqa: BLE001
        log.error("Shopify-data ei saatavilla: %s", e)
        print(f"::error::Konversiovartija ei saanut dataa: {e}")
        return 3

    today = next((r for r in rows if r.day == day), None)
    history = [r for r in rows if day - timedelta(days=7) <= r.day < day]
    if today is None:
        log.error("Päivälle %s ei ole sessiodataa (Shopify-analytiikka voi olla jäljessä).", day)
        print(f"::error::Päivälle {day} ei ole sessiodataa.")
        return 3

    v = judge(today, history, threshold, min_sessions)
    for line in v.lines:
        log.info(line)
    print(f"STATUS={v.status}")
    with open(os.getenv("GITHUB_OUTPUT", "/dev/null"), "a") as fh:
        fh.write(f"status={v.status}\n")
    summary = os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(f"## Konversiovartija {day.isoformat()} — {v.status}\n\n" + "\n".join(f"- {l}" for l in v.lines) + "\n")

    if v.status == "red":
        if a.dry_run:
            log.info("dry-run: WhatsApp-push ohitettu")
        else:
            run_url = None
            if os.getenv("GITHUB_SERVER_URL") and os.getenv("GITHUB_REPOSITORY") and os.getenv("GITHUB_RUN_ID"):
                run_url = f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
            sent = send_push(v, run_url)
            log.info("WhatsApp-push %s", "lähetetty" if sent else "EI lähtenyt (ks. loki)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

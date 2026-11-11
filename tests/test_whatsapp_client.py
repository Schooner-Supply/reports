"""
test_whatsapp_client.py — Yksikkötestit WhatsApp-ilmoituksen puhtaalle logiikalle

Ei verkkoa: testataan vastaanottajien jäsennys, pohjaparametrit, vapaa teksti
ja Cloud API -payloadit. Lähetys (requests.post) jää verkkotestien ulkopuolelle.
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import whatsapp_client as wa


REPORT_DATE = date(2026, 10, 21)   # keskiviikko
SUMMARY = ["12 tilausta, 1 450 € (+8 % vs 7 pv)", "Palautuksia 0", "Maksuongelmia 2"]


def test_parse_recipients_normalizes_and_dedupes():
    assert wa.parse_recipients("+358 40 123 4567, 040 1234567, 0046 70 123 45 67,,") == [
        "358401234567",
        "46701234567",
    ]
    assert wa.parse_recipients("") == []


def test_to_wa_id_variants():
    assert wa.to_wa_id("+358401234567") == "358401234567"
    assert wa.to_wa_id("040-1234567") == "358401234567"
    assert wa.to_wa_id("358401234567") == "358401234567"
    assert wa.to_wa_id("") == ""


def test_format_date_finnish_weekday():
    assert wa.format_date(REPORT_DATE) == "Ke 21.10.2026"


def test_template_params_four_single_line_values():
    params = wa.template_params(REPORT_DATE, "red", SUMMARY, "Tarkista maksut", "https://app.clickup.com/t/abc", 2)
    assert len(params) == 4
    assert params[0] == "Ke 21.10.2026"
    assert params[1] == "🔴 Toimenpiteitä"
    assert "12 tilausta" in params[2] and "⚠️ 2 alerttia" in params[2] and "Suositus: Tarkista maksut" in params[2]
    assert params[3] == "https://app.clickup.com/t/abc"
    for p in params:
        assert "\n" not in p and "\t" not in p
        assert len(p) <= wa.PARAM_MAX


def test_template_params_without_data():
    params = wa.template_params(REPORT_DATE, "yellow", [], "", None, 0)
    assert params[2] == "Ei tilauksia."
    assert params[3] == "-"


def test_template_params_truncate_long_summary():
    params = wa.template_params(REPORT_DATE, "red", ["x" * 2000], "", None, 0)
    assert len(params[2]) == wa.PARAM_MAX
    assert params[2].endswith("…")


def test_build_text_contains_sections():
    text = wa.build_text(REPORT_DATE, "yellow", SUMMARY, "Seuraa maksuja", "https://app.clickup.com/t/abc", 1)
    assert text.startswith("*Shopify-päiväraportti Ke 21.10.2026* — 🟡 Huomioitavaa")
    assert "- 12 tilausta" in text
    assert "⚠️ Alertteja: 1 kpl" in text
    assert "*Suositus:* Seuraa maksuja" in text
    assert text.rstrip().endswith("https://app.clickup.com/t/abc")
    assert len(text) <= wa.TEXT_MAX


def test_build_text_payload():
    p = wa.build_text_payload("+358 40 123 4567", "Hei")
    assert p == {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "358401234567",
        "type": "text",
        "text": {"preview_url": False, "body": "Hei"},
    }


def test_build_template_payload():
    p = wa.build_template_payload("358401234567", "shopify_daily_report", "fi", ["a", "b"])
    assert p["type"] == "template"
    assert p["to"] == "358401234567"
    assert p["template"]["name"] == "shopify_daily_report"
    assert p["template"]["language"] == {"code": "fi"}
    assert p["template"]["components"] == [
        {"type": "body", "parameters": [{"type": "text", "text": "a"}, {"type": "text", "text": "b"}]}
    ]
    assert wa.build_template_payload("358401234567", "hello", "fi", [])["template"]["components"] == []


def test_send_skips_when_not_configured(monkeypatch):
    for k in ("WHATSAPP_ACCESS_TOKEN", "WHATSAPP_PHONE_NUMBER_ID", "WHATSAPP_ALERT_RECIPIENTS"):
        monkeypatch.delenv(k, raising=False)
    assert wa.send_report_notification(REPORT_DATE, "red", SUMMARY, "x") is False


def test_send_skips_green_by_default(monkeypatch):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "t")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "1")
    monkeypatch.setenv("WHATSAPP_ALERT_RECIPIENTS", "+358401234567")
    monkeypatch.delenv("WHATSAPP_NOTIFY_GREEN", raising=False)
    calls = []
    monkeypatch.setattr(wa.requests, "post", lambda *a, **k: calls.append(a) or (_ for _ in ()).throw(AssertionError("ei saa kutsua")))
    assert wa.send_report_notification(REPORT_DATE, "green", SUMMARY, "x") is False
    assert calls == []


def test_send_uses_template_and_reports_success(monkeypatch):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "t")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "1")
    monkeypatch.setenv("WHATSAPP_ALERT_RECIPIENTS", "+358401234567,+358407654321")
    monkeypatch.setenv("WHATSAPP_REPORT_TEMPLATE", "shopify_daily_report")
    sent = []

    class Resp:
        ok = True
        status_code = 200
        text = "{}"

        def json(self):
            return {"messages": [{"id": "wamid.X"}]}

    def fake_post(url, json=None, headers=None, timeout=None):
        sent.append((url, json, headers))
        return Resp()

    monkeypatch.setattr(wa.requests, "post", fake_post)
    assert wa.send_report_notification(REPORT_DATE, "red", SUMMARY, "x", "https://app.clickup.com/t/abc", 1) is True
    assert len(sent) == 2
    url, payload, headers = sent[0]
    assert url == "https://graph.facebook.com/v21.0/1/messages"
    assert headers["Authorization"] == "Bearer t"
    assert payload["type"] == "template"
    assert payload["template"]["name"] == "shopify_daily_report"
    assert sent[1][1]["to"] == "358407654321"


def test_send_window_closed_is_logged_not_raised(monkeypatch, caplog):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "t")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "1")
    monkeypatch.setenv("WHATSAPP_ALERT_RECIPIENTS", "+358401234567")
    monkeypatch.delenv("WHATSAPP_REPORT_TEMPLATE", raising=False)

    class Resp:
        ok = False
        status_code = 400
        text = '{"error":{"code":131047}}'

        def json(self):
            return {"error": {"code": 131047, "message": "Re-engagement message"}}

    monkeypatch.setattr(wa.requests, "post", lambda *a, **k: Resp())
    with caplog.at_level("WARNING"):
        assert wa.send_report_notification(REPORT_DATE, "red", SUMMARY, "x") is False
    assert "24 h ikkuna kiinni" in caplog.text

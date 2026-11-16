"""Yksikkötestit konversiovartijan puhtaalle logiikalle (ei verkkoa)."""
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import conversion_guard as cg

D = date(2026, 11, 15)


def hist(days=7, sessions=100, cart=6, orders=2):
    return [cg.DayRow(D - timedelta(days=i), sessions, cart, orders) for i in range(1, days + 1)]


def test_green_when_rates_hold():
    v = cg.judge(cg.DayRow(D, 100, 6, 2), hist())
    assert v.status == "green"
    assert v.cart_rate == 0.06 and abs(v.cart_ref - 0.06) < 1e-9


def test_red_when_cart_rate_drops_over_half():
    v = cg.judge(cg.DayRow(D, 120, 2, 2), hist())   # 1.7 % vs 6 % = -72 %
    assert v.status == "red"
    assert "korilisäykset/sessio" in v.lines[0]


def test_red_when_order_rate_drops_over_half():
    v = cg.judge(cg.DayRow(D, 100, 6, 0), hist(orders=2))
    assert v.status == "red"
    assert "tilaukset/sessio" in v.lines[0]


def test_order_drop_alone_needs_enough_orders_in_history():
    # 7 pv aikana vain 2 tilausta -> 0 tilausta eilen ei riitä hälytykseen.
    v = cg.judge(cg.DayRow(D, 100, 6, 0), hist(orders=0) + [])
    assert v.status == "green"


def test_yellow_when_too_few_sessions():
    v = cg.judge(cg.DayRow(D, 10, 0, 0), hist())
    assert v.status == "yellow"


def test_yellow_when_history_too_short():
    v = cg.judge(cg.DayRow(D, 100, 0, 0), hist(days=2))
    assert v.status == "yellow"


def test_exactly_fifty_percent_is_not_an_alert():
    v = cg.judge(cg.DayRow(D, 100, 3, 1), hist())  # -50 % tasan
    assert v.status == "green"


def test_parse_rows_dict_and_list_shapes():
    table = {"columns": [{"name": "day"}, {"name": "sessions"}, {"name": "sessions_with_cart_additions"}, {"name": "sessions_that_completed_checkout"}],
             "rows": [{"day": "2026-11-14T00:00:00", "sessions": "120", "sessions_with_cart_additions": "7", "sessions_that_completed_checkout": "1"},
                      ["2026-11-13", 90, 5, 0]]}
    rows = cg.parse_shopifyql_rows(table)
    assert [r.day for r in rows] == [date(2026, 11, 13), date(2026, 11, 14)]
    assert rows[1].sessions == 120 and rows[1].cart_sessions == 7 and rows[1].order_sessions == 1


def test_build_query_quotes_countries():
    q = cg.build_query(date(2026, 11, 8), date(2026, 11, 15), ["Finland", "Åland Islands"])
    assert "session_country IN ('Finland', 'Åland Islands')" in q
    assert "SINCE 2026-11-08 UNTIL 2026-11-15" in q


# ── Liikenne maittain/kanavittain (lisätty 16.11.2026) ───────────────────────

from conversion_guard import SegRow, build_traffic_query, judge_traffic, parse_traffic_rows  # noqa: E402


def _seg(day, country, source, per_day, days=7):
    """Tasainen historia: per_day sessiota joka päivä 7 pv ennen `day`."""
    return [SegRow(day - timedelta(days=i), country, source, per_day) for i in range(1, days + 1)]


def test_traffic_red_when_country_channel_drops_over_40_percent():
    d = date(2026, 11, 12)
    rows = _seg(d, "Finland", "search", 50) + _seg(d, "Finland", "direct", 40)
    rows += [SegRow(d, "Finland", "search", 11), SegRow(d, "Finland", "direct", 41)]
    status, lines = judge_traffic(d, rows)
    assert status == "red"
    assert "Finland × search 11 vs ka 50 (−78 %)" in lines[0]
    assert "kanava search" in lines[0]
    assert "direct" not in lines[0].split(";")[0]  # direct ei pudonnut


def test_traffic_green_when_within_threshold():
    d = date(2026, 11, 12)
    rows = _seg(d, "Finland", "search", 50) + [SegRow(d, "Finland", "search", 35)]  # −30 %
    status, lines = judge_traffic(d, rows)
    assert status == "green"
    assert any(l.startswith("Finland: 35 sessiota") for l in lines)


def test_traffic_ignores_thin_segments():
    d = date(2026, 11, 12)
    rows = _seg(d, "Sweden", "social", 3)  # ka 3/pv, putoaa nollaan — kohinaa
    status, _ = judge_traffic(d, rows)
    assert status == "green"


def test_traffic_missing_day_counts_as_zero():
    d = date(2026, 11, 12)
    rows = _seg(d, "Finland", "search", 70)  # tänään ei riviä = 0 sessiota
    status, lines = judge_traffic(d, rows)
    assert status == "red"
    assert "−100 %" in lines[0]


def test_traffic_yellow_when_history_short():
    d = date(2026, 11, 12)
    rows = _seg(d, "Finland", "search", 50, days=2)
    status, lines = judge_traffic(d, rows)
    assert status == "yellow"


def test_parse_traffic_rows_and_query():
    table = {"columns": [{"name": "day"}, {"name": "session_country"}, {"name": "referrer_source"}, {"name": "sessions"}],
             "rows": [["2026-11-13", "Finland", "search", "16"], {"day": "2026-11-13", "session_country": "Sweden", "referrer_source": "direct", "sessions": 4}]}
    rows = parse_traffic_rows(table)
    assert [(r.country, r.source, r.sessions) for r in rows] == [("Finland", "search", 16), ("Sweden", "direct", 4)]
    q = build_traffic_query(date(2026, 11, 5), date(2026, 11, 12), ["Finland", "Åland Islands"])
    assert "GROUP BY session_country, referrer_source" in q and "'Åland Islands'" in q and "TIMESERIES day" in q

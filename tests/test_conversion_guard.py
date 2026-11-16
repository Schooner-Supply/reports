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

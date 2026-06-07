from decimal import Decimal
from utils.order import CalcTotalPrice


def test_calc_total_price_success():
    calc = CalcTotalPrice()

    price_map = {
        1: Decimal("100.50"),
        2: Decimal("50.00"),
        3: Decimal("10.25")
    }

    quantity_map = {
        1: 2,
        2: 1,
        3: 4
    }

    result = calc(price_map, quantity_map)

    assert result == Decimal("292.00")


def test_calc_total_price_rounding():
    calc = CalcTotalPrice()

    price_map = {1: Decimal("10.333")}
    quantity_map = {1: 3}

    result = calc(price_map, quantity_map)

    assert result == Decimal("31.00")

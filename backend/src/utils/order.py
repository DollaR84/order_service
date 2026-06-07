from decimal import Decimal, ROUND_HALF_UP


class CalcTotalPrice:

    def __init__(self) -> None:
        self.two_places = Decimal("0.01")

    def __call__(self, price_map: dict[int, Decimal], quantity_map: dict[int, int]) -> Decimal:
        result = Decimal("0.00")

        for product_id, price in price_map.items():
            product_price = Decimal(str(price))
            quantity = Decimal(quantity_map[product_id])

            item_total = product_price * quantity
            result += item_total

        return result.quantize(self.two_places, rounding=ROUND_HALF_UP)

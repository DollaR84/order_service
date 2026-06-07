class ApplicationError(Exception):
    pass


class NotEnoughStockError(ApplicationError):

    def __init__(self, product_id: int, available: int, requested: int):
        self.product_id = product_id
        self.available = available
        self.requested = requested

        super().__init__(
            f"Not enough stock for product #{product_id}. "
            f"Available: {available}, requested: {requested}."
        )

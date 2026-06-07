from enum import StrEnum


class OrderStatusType(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

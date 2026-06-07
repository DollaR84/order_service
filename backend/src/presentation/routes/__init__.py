from .auth import bp as bp_auth
from .client import bp as bp_client
from .order import bp as bp_order
from .product import bp as bp_product
from .root import bp as bp_root


__all__ = (
    "bp_auth",
    "bp_client",
    "bp_order",
    "bp_product",
    "bp_root",
)

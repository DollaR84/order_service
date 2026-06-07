from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


class ClientToOrderSchema(BaseModel):
    client_id: Optional[int] = None


class CreateOrderItemSchema(BaseModel):
    product_id: int
    quantity: int


class CreateOrderSchema(BaseModel):
    client_id: int
    items: list[CreateOrderItemSchema] = Field(..., min_length=1)

    @model_validator(mode="before")
    @classmethod
    def parse_flat_form_data(cls, data: Any) -> Any:
        if isinstance(data, dict) and "items" in data:
            return data

        if not isinstance(data, dict):
            return data

        client_id = data.get("client_id")
        items = []
        for key, value in data.items():
            if key.startswith("product_") and value == "on":
                try:
                    product_id = int(key.split("_")[1])

                    qty_key = f"qty_{product_id}"
                    quantity = int(data.get(qty_key, 1))

                    items.append({
                        "product_id": product_id,
                        "quantity": quantity
                    })
                except (ValueError, IndexError):
                    continue

        return {
            "client_id": client_id,
            "items": items,
        }

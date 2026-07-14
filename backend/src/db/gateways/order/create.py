from sqlalchemy import insert, select, update

from application.exceptions import NotEnoughStockError
from db import domain
from utils.order import CalcTotalPrice

from ..base import BaseGateway
from ...models import Order, OrderItem, Product


class CreateOrderGateway(BaseGateway[int, Order]):

    async def create_order(self, data: domain.NewOrderModel) -> int:
        calc = CalcTotalPrice()
        product_ids = [item.product_id for item in data.items]
        quantity_map = {item.product_id: item.quantity for item in data.items}

        select_stmt = (
            select(Product.id, Product.price, Product.stock)
            .where(Product.id.in_(product_ids))
            .with_for_update()
        )
        result = await self.session.execute(select_stmt)

        price_map, stock_map = {}, {}
        for pid, price, stock in result.all():
            price_map[pid] = price
            stock_map[pid] = stock
            if stock < quantity_map[pid]:
                raise NotEnoughStockError(product_id=pid, available=stock, requested=quantity_map[pid])

        stmt = insert(Order)
        stmt = stmt.values(
            client_id=data.client_id,
            total_price=calc(price_map, quantity_map),
            status=data.status,
        )
        stmt = stmt.returning(Order.id)

        result = await self.session.execute(stmt)
        order_id: int = result.scalar_one()

        items_values = []
        for item in data.items:
            price = price_map.get(item.product_id)

            if price is None:
                raise ValueError(f"Product not found: {item.product_id}")

            items_values.append({
                "order_id": order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_time": price,
            })

        stmt = insert(OrderItem).values(items_values)
        await self.session.execute(stmt)

        update_data = [
            {"id": pid, "stock": stock - quantity_map[pid]}
            for pid, stock in stock_map.items()
        ]
        update_stmt = update(Product)
        await self.session.execute(update_stmt, update_data)

        return order_id

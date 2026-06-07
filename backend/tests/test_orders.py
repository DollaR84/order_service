from decimal import Decimal

import pytest
from sqlalchemy import select

from application import dto, interactors
from application.exceptions import NotEnoughStockError
from application.types import OrderStatusType
from db.gateways import CreateOrderGateway
from db.models import Product, Order


@pytest.mark.asyncio
async def test_create_order_success(db_session):
    product = Product(id=1, name="coffee machine", price=Decimal("500.00"), stock=10)
    db_session.add(product)
    await db_session.commit()

    gateway = CreateOrderGateway(db_session)
    interactor = interactors.CreateOrder(gateway)

    order_data = dto.NewOrder(
        client_id=1,
        status=OrderStatusType.PENDING,
        items=[
            dto.NewOrderItem(product_id=1, quantity=3)
        ]
    )

    order_id = await interactor(order_data)

    assert order_id is not None

    await db_session.refresh(product)
    assert product.stock == 7

    result = await db_session.execute(select(Order).where(Order.id == order_id))
    saved_order = result.scalar_one()
    assert saved_order.total_price == Decimal("1500.00")


@pytest.mark.asyncio
async def test_create_order_raises_not_enough_stock(db_session):
    product = Product(id=2, name="bean coffee", price=Decimal("50.00"), stock=2)
    db_session.add(product)
    await db_session.commit()

    gateway = CreateOrderGateway(session=db_session)
    interactor = interactors.CreateOrder(gateway)

    order_data = dto.NewOrder(
        client_id=1,
        status=OrderStatusType.PENDING,
        items=[
            dto.NewOrderItem(product_id=2, quantity=5)
        ]
    )

    with pytest.raises(NotEnoughStockError) as exc_info:
        await interactor(order_data)

    assert exc_info.value.product_id == 2
    assert exc_info.value.requested == 5
    assert exc_info.value.available == 2

    await db_session.refresh(product)
    assert product.stock == 2

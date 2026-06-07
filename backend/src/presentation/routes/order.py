from flask import Blueprint, flash, redirect, render_template, url_for
from flask.typing import ResponseReturnValue
from flask.views import MethodView
from flask_login import login_required

from application import dto, interactors
from application.exceptions import NotEnoughStockError
from core.di import inject, FromDishka
from utils.http import parse_request

from .. import schemas


bp = Blueprint("orders", __name__, url_prefix="/orders")


class OrdersView(MethodView):

    @login_required
    @inject
    async def get(self, interactor: FromDishka[interactors.GetOrders]) -> ResponseReturnValue:
        try:
            data = parse_request(schemas.ClientToOrderSchema)
        except ValueError:
            data = schemas.ClientToOrderSchema()

        orders = await interactor(data.client_id)

        return render_template(
            "orders/index.html",
            orders=orders
        )


class CreateOrderFormView(MethodView):

    @login_required
    @inject
    async def get(
            self,
            get_clients: FromDishka[interactors.GetClients],
            get_products: FromDishka[interactors.GetProducts],
    ) -> ResponseReturnValue:
        try:
            data = parse_request(schemas.ClientToOrderSchema)
        except ValueError:
            data = schemas.ClientToOrderSchema()

        clients = await get_clients(dto.ClientSearchFilters())
        products = await get_products()

        return render_template(
            "orders/new.html",
            selected_client_id=data.client_id,
            clients=clients,
            products=products
        )

    @login_required
    @inject
    async def post(self, creator: FromDishka[interactors.CreateOrder]) -> ResponseReturnValue:
        try:
            data = parse_request(schemas.CreateOrderSchema)
        except ValueError as e:
            flash(f"Please select at client or least one product with a valid quantity.\n{e}", "danger")
            return redirect(url_for("orders.new"))

        order_data = dto.NewOrder(
            client_id=data.client_id,
            items=[
                dto.NewOrderItem(**item.model_dump())
                for item in data.items
            ],
        )

        try:
            await creator(order_data)

            flash("Order created successfully!", "success")
            return redirect(url_for("orders.index"))

        except NotEnoughStockError as e:
            flash(f"Failed to process order: {e}", "danger")
            return redirect(url_for("orders.new"))

        except Exception:
            flash("Something went wrong on the server", "danger")
            return redirect(url_for("orders.new"))


class OrderDetailView(MethodView):

    @login_required
    @inject
    async def get(
            self,
            order_id: int,
            get_order: FromDishka[interactors.GetOrder],
            get_client: FromDishka[interactors.GetClientByID],
    ) -> ResponseReturnValue:
        order = await get_order(order_id)
        if not order:
            flash(f"Order #{order_id} not found", "warning")
            return redirect(url_for("orders.index"))

        client = await get_client(order.client_id)
        return render_template(
            "orders/detail.html",
            order=order,
            client=client
        )


bp.add_url_rule("/", view_func=OrdersView.as_view("index"))
bp.add_url_rule("/new", view_func=CreateOrderFormView.as_view("new"))
bp.add_url_rule("/<int:order_id>", view_func=OrderDetailView.as_view("detail"))

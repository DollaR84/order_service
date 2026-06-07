from flask import Blueprint, flash, redirect, render_template, url_for
from flask.views import MethodView
from flask.typing import ResponseReturnValue
from flask_login import login_required

from application import dto, interactors
from core.di import inject, FromDishka
from utils.http import parse_request

from .. import schemas


bp = Blueprint("products", __name__, url_prefix="/products")


class ProductsView(MethodView):

    @login_required
    @inject
    async def get(self, interactor: FromDishka[interactors.GetProducts]) -> ResponseReturnValue:
        try:
            filters = parse_request(schemas.SearchProductSchema)
        except ValueError as e:
            flash(f"Validation error: {e}", "danger")
            filters = schemas.SearchProductSchema()

        products = await interactor(
            name=filters.name,
            description=filters.description,
        )

        return render_template(
            "products/index.html",
            products=products,
            filters=filters.model_dump()
        )


class CreateProductView(MethodView):

    @login_required
    @inject
    async def get(self) -> ResponseReturnValue:
        return render_template("products/new.html")

    @login_required
    @inject
    async def post(self, creator: FromDishka[interactors.CreateProduct]) -> ResponseReturnValue:
        try:
            data = parse_request(schemas.CreateProductSchema)
        except ValueError as e:
            flash(f"Validation error: {e}", "danger")
            return redirect(url_for("products.new"))

        try:
            product = dto.NewProduct(
                name=data.name,
                description=data.description or None,
                price=data.price,
                stock=data.stock or 0,
            )
            product_id = await creator(product)

            flash("Product created successfully", "success")
            return redirect(url_for("products.detail", product_id=product_id))

        except Exception:
            flash("Invalid product data", "danger")
            return redirect(url_for("products.new"))


class ProductView(MethodView):

    @login_required
    @inject
    async def get(
            self,
            product_id: int,
            interactor: FromDishka[interactors.GetProduct],
    ) -> ResponseReturnValue:
        product = await interactor(product_id)
        if not product:
            flash(f"Product #{product_id} not found", "warning")
            return redirect(url_for("products.index"))

        return render_template("products/detail.html", product=product)


bp.add_url_rule("/", view_func=ProductsView.as_view("index"))
bp.add_url_rule("/new", view_func=CreateProductView.as_view("new"))
bp.add_url_rule("/<int:product_id>", view_func=ProductView.as_view("detail"))

from flask import Blueprint, flash, redirect, render_template, url_for
from flask.views import MethodView
from flask.typing import ResponseReturnValue
from flask_login import login_required

from application import dto, interactors
from core.di import inject, FromDishka
from utils.http import parse_request

from .. import schemas


bp = Blueprint("clients", __name__, url_prefix="/clients")


class ClientsView(MethodView):

    @login_required
    @inject
    async def get(self, interactor: FromDishka[interactors.GetClients]) -> ResponseReturnValue:
        try:
            filters = parse_request(schemas.SearchClientSchema)
        except ValueError as e:
            flash(f"Validation error: {e}", "danger")
            filters = schemas.SearchClientSchema()

        clients = await interactor(
            dto.ClientSearchFilters(
                phone=filters.phone,
                email=filters.email,
                first_name=filters.first_name,
                last_name=filters.last_name,
            )
        )

        return render_template(
            "clients/index.html",
            clients=clients,
            filters=filters.model_dump()
        )


class CreateClientView(MethodView):

    @login_required
    @inject
    async def get(self) -> ResponseReturnValue:
        return render_template("clients/new.html")

    @login_required
    @inject
    async def post(self, creator: FromDishka[interactors.CreateClient]) -> ResponseReturnValue:
        try:
            data = parse_request(schemas.CreateClientSchema)
        except ValueError as e:
            flash(f"Validation error: {e}", "danger")
            return redirect(url_for("clients.new"))

        try:
            client = dto.NewClient(
                phone=data.phone,
                email=data.email or None,
                first_name=data.first_name or None,
                last_name=data.last_name or None,
            )
            client_id = await creator(client)

            flash("Client created successfully", "success")
            return redirect(url_for("clients.detail", client_id=client_id))

        except Exception:
            flash("Invalid client data", "danger")
            return redirect(url_for("clients.new"))


class ClientView(MethodView):

    @login_required
    @inject
    async def get(
            self,
            client_id: int,
            interactor: FromDishka[interactors.GetClientByID],
    ) -> ResponseReturnValue:
        client = await interactor(client_id)
        if not client:
            flash(f"Client #{client_id} not found", "warning")
            return redirect(url_for("clients.index"))

        return render_template("clients/detail.html", client=client)


bp.add_url_rule("/", view_func=ClientsView.as_view("index"))
bp.add_url_rule("/new", view_func=CreateClientView.as_view("new"))
bp.add_url_rule("/<int:client_id>", view_func=ClientView.as_view("detail"))

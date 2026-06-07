from flask import Blueprint, flash, redirect, render_template, url_for
from flask.typing import ResponseReturnValue
from flask.views import MethodView
from flask_login import login_required

from core.di import inject, FromDishka
from utils.http import parse_request

from .. import schemas
from ..auth import AuthManager


bp = Blueprint("auth", __name__, url_prefix="/")


class LoginView(MethodView):

    @inject
    async def get(self) -> ResponseReturnValue:
        return render_template("auth/login.html")

    @inject
    async def post(self, auth: FromDishka[AuthManager]) -> ResponseReturnValue:
        try:
            data = parse_request(schemas.AuthAdminSchema)
        except ValueError as e:
            flash(f"Validation error: {e}", "danger")
            return redirect(url_for("auth.login"))

        if auth.login(data.username, data.password):
            return redirect(url_for("orders.index"))

        flash("Invalid login or password", "danger")
        return redirect(url_for("auth.login"))


@bp.route("/logout", methods=["GET"])
@login_required
@inject
async def logout(auth: FromDishka[AuthManager]) -> ResponseReturnValue:
    auth.logout()
    flash("You have successfully logged out.", "success")
    return redirect(url_for("root.home"))


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))

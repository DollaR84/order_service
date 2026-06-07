from typing import Type, TypeVar, Any

from flask import request
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


def parse_request(schema: Type[T]) -> T:
    raw_data: dict[str, Any]

    if request.method == "GET":
        raw_data = request.args.to_dict()

    elif request.is_json:
        raw_data = request.get_json() or {}

    else:
        raw_data = request.form.to_dict()

    try:
        return schema.model_validate(raw_data)
    except ValidationError as e:
        raise ValueError(e.errors()) from e

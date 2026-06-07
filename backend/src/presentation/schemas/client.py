from typing import Any, Optional

from pydantic import BaseModel, EmailStr, model_validator

from utils.phone import PhoneNumber


class BaseClientSchema(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def empty_string_to_none(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: (None if v == "" else v) for k, v in data.items()}
        return data


class CreateClientSchema(BaseClientSchema):
    phone: PhoneNumber


class SearchClientSchema(BaseClientSchema):
    phone: Optional[str] = None

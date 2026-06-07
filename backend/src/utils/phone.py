import re
from typing import Annotated

from pydantic import AfterValidator


PHONE_REGEX = re.compile(r"^\+3\d{10,15}$")


def validate_phone_number(value: str) -> str:
    cleaned = re.sub(r"[^\+\d]", "", value)

    if not PHONE_REGEX.match(cleaned):
        raise ValueError(
            "Incorrect phone format. Expected: +38 (0XX) XXX-XX-XX"
        )
    return cleaned


PhoneNumber = Annotated[str, AfterValidator(validate_phone_number)]


def format_phone(phone_str: str) -> str:
    if not phone_str:
        return ""

    if len(phone_str) < 11 or len(phone_str) > 16:
        return phone_str

    if len(phone_str) == 13 and phone_str.startswith("+380"):
        return f"{phone_str[0:3]} ({phone_str[3:6]}) {phone_str[6:9]}-{phone_str[9:11]}-{phone_str[11:13]}"

    return f"{phone_str[0:2]} {phone_str[2:5]} {phone_str[5:]}"

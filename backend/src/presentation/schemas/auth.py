from pydantic import BaseModel


class AuthAdminSchema(BaseModel):
    username: str
    password: str

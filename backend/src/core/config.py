from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseModel):
    username: str
    password: str
    name: str
    host: str
    port: int = 5432
    debug: bool = False

    ssl: bool = False
    url: Optional[str] = None

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        if not 0 < value < 65535:
            raise ValueError("invalid db postgres port")
        return value

    @property
    def uri(self) -> str:
        uri = f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"
        return self.url if self.url else uri


class FlaskConfig(BaseModel):
    templates_dir: Path
    static_dir: Path


class AdminConfig(BaseModel):
    username: str
    password_hash: str
    secret_key: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    db: DBConfig
    flask: FlaskConfig
    admin: AdminConfig


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()

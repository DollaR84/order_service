from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseClient(BaseData):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    email: Optional[str] = None
    phone: str


@dataclass(slots=True, kw_only=True)
class NewClient(BaseClient):
    pass


@dataclass(slots=True)
class Client(BaseClient):
    id: int
    uuid_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return " ".join([self.first_name, self.last_name])
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        return ""


@dataclass(slots=True)
class ClientSearchFilters(BaseData):
    phone: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

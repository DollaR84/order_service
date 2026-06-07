from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseClientModel(BaseData):
    phone: str
    email: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass(slots=True)
class NewClientModel(BaseClientModel):
    pass


@dataclass(slots=True)
class ClientModel(BaseClientModel):
    id: int
    uuid_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class ItemCreate(SQLModel):
    title: str
    description: str | None = None


class ItemUpdate(SQLModel):
    title: str | None = None
    description: str | None = None


class ItemPublic(SQLModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int

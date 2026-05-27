import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserRegister(SQLModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: EmailStr | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


class UserPublic(SQLModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    full_name: str | None = None
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

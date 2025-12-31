from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, EmailStr, Field

from guard.schemas import BaseModel, Paginate
from guard.validators.password import validate_login_password

PasswordStr = Annotated[
    str, Field(min_length=8, max_length=30), AfterValidator(validate_login_password)
]


class CreateUserParams(BaseModel):
    email: EmailStr
    password: PasswordStr


class UpdateUserParams(BaseModel):
    name: Annotated[str | None, Field(min_length=2, max_length=10)] = None
    is_active: bool | None = None


class _UserBase(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str | None = None
    is_active: bool
    created_at: datetime


class CreateUser(_UserBase):
    pass


class GetUser(_UserBase):
    email_verified: bool
    phone_verified: bool


class ListUser(Paginate):
    items: list[GetUser]


class UpdateUser(GetUser):
    updated_at: datetime

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from guard.schemas import BaseModel, Paginate


class CreateRoleParams(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=200)]
    default: bool | None = None


class UpdateRoleParams(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=200)] = None
    default: bool | None = None


class _RoleBase(BaseModel):
    id: UUID
    name: str
    default: bool
    created_at: datetime


class CreateRole(_RoleBase):
    pass


class GetRole(_RoleBase):
    pass


class ListRole(Paginate):
    items: list[GetRole]


class UpdateRole(GetRole):
    updated_at: datetime

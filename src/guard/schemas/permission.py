from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from guard.schemas import BaseModel, Paginate

_CreatePermissionStr = Annotated[str, Field(min_length=1, max_length=200)]


class CreatePermissionParams(BaseModel):
    name: _CreatePermissionStr
    code: _CreatePermissionStr


_UpdatePermissionStr = Annotated[str | None, Field(min_length=1, max_length=200)]


class UpdatePermissionParams(BaseModel):
    name: _UpdatePermissionStr = None
    code: _UpdatePermissionStr = None


class _PermissionBase(BaseModel):
    id: UUID
    name: str
    code: str
    created_at: datetime


class CreatePermission(_PermissionBase):
    pass


class GetPermission(_PermissionBase):
    pass


class ListPermission(Paginate):
    items: list[GetPermission]


class UpdatePermission(GetPermission):
    updated_at: datetime

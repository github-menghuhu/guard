from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from guard.schemas import BaseModel, Paginate


class CreatePermissionParams(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=200, description="权限名称")]
    code: Annotated[str, Field(min_length=1, max_length=200, description="权限标识")]


class UpdatePermissionParams(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=200, description="权限名称")] = None
    code: Annotated[str | None, Field(min_length=1, max_length=200, description="权限标识")] = None


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

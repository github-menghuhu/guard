from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from guard.schemas import BaseModel, Paginate


class CreateRoleParams(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=200, description="角色名称")]
    default: Annotated[bool, Field(description="是否为基础用户默认角色")]


class UpdateRoleParams(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=200, description="角色名称")] = None
    default: Annotated[bool | None, Field(description="是否为基础用户默认角色")] = None


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

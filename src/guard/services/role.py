from uuid import UUID

from guard.models import Role
from guard.repositories import RoleRepository
from guard.schemas import CreateRole, GetRole, ListRole, UpdateRole
from guard.services.base import BaseService


class RoleService(BaseService[RoleRepository, Role]):
    async def create(self, name: str, default: bool | None = None) -> CreateRole:
        role = Role(name=name)

        if default is not None:
            role.default = default

        role = await self.repository.create(role)
        return CreateRole.model_validate(role)

    async def list_paginate(
        self,
        name: str | None = None,
        default: bool | None = None,
        page: int = 1,
        size: int = 10,
    ) -> ListRole:
        items = await self.repository.list_paginate(name, default, page, size)
        return ListRole.model_validate(items)

    async def get(self, id_: UUID) -> GetRole:
        role = await self.validate_id_exist(id_)
        return GetRole.model_validate(role)

    async def update(
        self,
        id_: UUID,
        name: str | None = None,
        default: bool | None = None,
    ) -> UpdateRole:
        role = await self.validate_id_exist(id_)

        if name:
            role.name = name

        if default is not None:
            role.default = default

        role = await self.repository.update(role)
        return UpdateRole.model_validate(role)

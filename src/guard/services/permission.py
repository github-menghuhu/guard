from uuid import UUID

from guard.models import Permission
from guard.repositories import PermissionRepository
from guard.schemas import (
    CreatePermission,
    GetPermission,
    ListPermission,
    UpdatePermission,
)
from guard.services.base import BaseService


class PermissionService(BaseService[PermissionRepository, Permission]):
    async def create(self, name: str, code: str) -> CreatePermission:
        permission = Permission(name=name, code=code)
        permission = await self.repository.create(permission)
        return CreatePermission.model_validate(permission)

    async def list_paginate(
        self,
        name: str | None = None,
        code: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> ListPermission:
        items = await self.repository.list_paginate(name, code, page, size)
        return ListPermission.model_validate(items)

    async def get(self, id_: UUID) -> GetPermission:
        permission = await self.validate_id_exist(id_)
        return GetPermission.model_validate(permission)

    async def update(
        self,
        id_: UUID,
        name: str | None = None,
        code: str | None = None,
    ) -> UpdatePermission:
        permission = await self.validate_id_exist(id_)

        if name:
            permission.name = name

        if code is not None:
            permission.code = code

        permission = await self.repository.update(permission)
        return UpdatePermission.model_validate(permission)

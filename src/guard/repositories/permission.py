from sqlalchemy import select

from guard.models import Permission
from guard.repositories import BaseRepository, Paginate


class PermissionRepository(BaseRepository[Permission]):
    _model = Permission

    async def list_paginate(
        self,
        name: str | None = None,
        code: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> Paginate[Permission]:
        statement = select(self._model).order_by(self._model.created_at.desc())

        if name:
            statement = statement.where(self._model.name.like(f"%{name}%"))

        if code:
            statement = statement.where(self._model.code.like(f"%{code}%"))

        return await self._paginate(statement, page, size)

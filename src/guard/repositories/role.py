from sqlalchemy import select

from guard.models import Role
from guard.repositories import BaseRepository, Paginate


class RoleRepository(BaseRepository[Role]):
    _model = Role

    async def list_paginate(
        self,
        name: str | None = None,
        default: bool | None = None,
        page: int = 1,
        size: int = 10,
    ) -> Paginate[Role]:
        statement = select(self._model).order_by(self._model.created_at.desc())

        if name:
            statement = statement.where(self._model.name.like(f"%{name}%"))

        if default is not None:
            statement = statement.where(self._model.default.is_(default))

        return await self._paginate(statement, page, size)

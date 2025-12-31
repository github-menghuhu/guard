from sqlalchemy import select

from guard.models import OAuthProvider
from guard.repositories import BaseRepository, Paginate


class OAuthProviderRepository(BaseRepository[OAuthProvider]):
    _model = OAuthProvider

    async def list_paginate(
        self,
        name: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> Paginate[OAuthProvider]:
        statement = select(self._model).order_by(self._model.created_at.desc())

        if name:
            statement = statement.where(self._model.provider_name.like(f"%{name}%"))

        return await self._paginate(statement, page, size)

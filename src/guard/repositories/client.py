from sqlalchemy import select

from guard.models import Client
from guard.repositories import BaseRepository, Paginate


class ClientRepository(BaseRepository[Client]):
    _model = Client

    async def list_paginate(
        self,
        name: str | None = None,
        creator: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> Paginate:
        statement = select(Client).order_by(Client.created_at.desc())

        if name:
            statement = statement.where(Client.client_name.like(f"%{name}%"))

        if creator:
            statement = statement.where(Client.creator.like(f"%{creator}%"))

        return await self._paginate(statement, page, size)

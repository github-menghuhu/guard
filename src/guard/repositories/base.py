from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from guard.dependencies import get_async_session


class BaseRepository[M]:
    model: M

    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_async_session)]
    ) -> None:
        self.session = session

    async def _execute(self, statement: Select) -> Result:
        return await self.session.execute(statement)

    async def list(self) -> list[M]:
        pass

    async def get(self, id_: UUID) -> M | None:
        result = await self._execute(select(self.model).where(self.model.id == id_))
        return result.scalar_one_or_none()

    async def create(self, object_: M) -> M:
        self.session.add(object_)
        await self.session.commit()
        await self.session.refresh(object_)
        return object_

    async def update(self, object_: M) -> None:
        self.session.add(object_)
        await self.session.commit()

    async def delete(self, object_: M) -> None:
        await self.session.delete(object_)
        await self.session.commit()

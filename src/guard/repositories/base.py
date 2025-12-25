from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import Select

M = TypeVar("M", bound=DeclarativeBase)


class BaseRepository[M]:
    _model: type[M]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _execute(self, statement: Select) -> Result:
        return await self.session.execute(statement)

    async def list(self) -> list[M]:
        pass

    async def get(self, id_: UUID) -> M | None:
        result = await self._execute(select(self._model).where(self._model.id == id_))  # type: ignore[attr-defined]
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

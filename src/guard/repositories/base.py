from typing import TypedDict
from uuid import UUID

from sqlalchemy import func, over, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from guard.models.base import Base


class Paginate[I](TypedDict):
    total: int
    page: int
    size: int
    items: list[I]


class BaseRepository[M: Base]:
    _model: type[M]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _execute(self, statement: Select) -> Result:
        return await self.session.execute(statement)

    async def _paginate(
        self,
        statement: Select,
        page: int = 1,
        size: int = 10,
    ) -> Paginate:
        statement = statement.offset((page - 1) * size).limit(size)
        statement = statement.add_columns(over(func.count()))

        results: list[M] = []
        count = 0
        for row in await self._execute(statement):
            results.append(row[0])
            count = row[1]

        return {
            "total": count,
            "page": page,
            "size": size,
            "items": results,
        }

    async def get(self, id_: UUID) -> M | None:
        result = await self._execute(select(self._model).where(self._model.id == id_))  # type: ignore[attr-defined]
        return result.scalar_one_or_none()

    async def create(self, object_: M) -> M:
        self.session.add(object_)
        await self.session.commit()
        await self.session.refresh(object_)
        return object_

    async def update(self, object_: M) -> M:
        self.session.add(object_)
        await self.session.commit()
        await self.session.refresh(object_)
        return object_

    async def delete(self, object_: M) -> None:
        await self.session.delete(object_)
        await self.session.commit()

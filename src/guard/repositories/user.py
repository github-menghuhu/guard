from pydantic import EmailStr
from sqlalchemy import select

from guard.models import User
from guard.repositories import BaseRepository, Paginate


class UserRepository(BaseRepository[User]):
    _model = User

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        statement = select(self._model).where(self._model.email == email)
        result = await self._execute(statement)
        return result.scalar_one_or_none()

    async def list_paginate(
        self,
        name: EmailStr | None = None,
        email: str | None = None,
        phone: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> Paginate[User]:
        statement = select(self._model).order_by(self._model.created_at.desc())

        if name:
            statement = statement.where(self._model.name.like(f"%{name}%"))

        if phone:
            statement = statement.where(self._model.phone.like(f"%{phone}%"))

        if email:
            statement = statement.where(self._model.email.like(f"%{email}%"))

        return await self._paginate(statement, page, size)

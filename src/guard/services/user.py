from uuid import UUID

from api_exception import APIException
from fastapi import status
from pydantic import EmailStr

from guard.core.crypto import PasswordHasher
from guard.core.exception import ExceptionCode
from guard.models import User
from guard.repositories import UserRepository
from guard.schemas import CreateUser, GetUser, ListUser, UpdateUser
from guard.services.base import BaseService


class UserService(BaseService[UserRepository, User]):
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher
    ) -> None:
        super().__init__(repository)
        self.password_hasher = password_hasher

    async def validate_email_exists(self, email: EmailStr) -> None:
        user = await self.repository.get_user_by_email(email)
        if user is not None:
            raise APIException(
                http_status_code=status.HTTP_409_CONFLICT,
                error_code=ExceptionCode.CONFLICT_ERROR,
                message=f"Email {email} already exists",
            )
        return None

    async def create(
        self,
        email: EmailStr,
        password: str,
        name: str | None = None,
        phone: str | None = None,
    ) -> CreateUser:
        await self.validate_email_exists(email)
        user = User(email=email, password=self.password_hasher.hash(password))

        if name:
            user.name = name

        if phone:
            user.phone = phone

        user = await self.repository.create(user)
        return CreateUser.model_validate(user)

    async def list_paginate(
        self,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> ListUser:
        items = await self.repository.list_paginate(name, email, phone, page, size)
        return ListUser.model_validate(items)

    async def get(self, id_: UUID) -> GetUser:
        user = await self.validate_id_exist(id_)
        return GetUser.model_validate(user)

    async def update(
        self,
        id_: UUID,
        name: str | None = None,
        is_active: bool | None = None,
    ) -> UpdateUser:
        user = await self.validate_id_exist(id_)

        if name:
            user.name = name

        if is_active is not None:
            user.is_active = is_active

        user = await self.repository.update(user)
        return UpdateUser.model_validate(user)

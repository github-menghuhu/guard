from uuid import UUID

from api_exception import APIException
from fastapi import status
from pydantic import EmailStr

from guard.core.crypto import PasswordHasher
from guard.core.exception import ExceptionCode
from guard.models import User
from guard.repositories import UserRepository
from guard.schemas import CreateUser, GetUser, ListUser, UpdateUser


class UserService:
    def __init__(
        self, user_repository: UserRepository, password_hasher: PasswordHasher
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def validate_user_id(self, id_: UUID) -> User:
        user = await self.user_repository.get(id_)
        if user is None:
            raise APIException(
                http_status_code=status.HTTP_404_NOT_FOUND,
                error_code=ExceptionCode.NOT_FOUND,
            )
        return user

    async def validate_email_exists(self, email: EmailStr) -> None:
        user = await self.user_repository.get_user_by_email(email)
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

        user = await self.user_repository.create(user)
        return CreateUser.model_validate(user)

    async def list_paginate(
        self,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> ListUser:
        items = await self.user_repository.list_paginate(name, email, phone, page, size)
        return ListUser.model_validate(items)

    async def get(self, id_: UUID) -> GetUser:
        user = await self.validate_user_id(id_)
        return GetUser.model_validate(user)

    async def update(
        self,
        id_: UUID,
        name: str | None = None,
        is_active: bool | None = None,
    ) -> UpdateUser:
        user = await self.validate_user_id(id_)

        if name:
            user.name = name

        if is_active is not None:
            user.is_active = is_active

        user = await self.user_repository.update(user)

        client = await self.user_repository.update(user)
        return UpdateUser.model_validate(client)

    async def delete(self, id_: UUID) -> None:
        user = await self.validate_user_id(id_)
        await self.user_repository.delete(user)

from uuid import UUID

from api_exception import APIException
from fastapi import status

from guard.core.exception import ExceptionCode
from guard.models import Base
from guard.repositories import BaseRepository


class BaseService[R: BaseRepository, M: Base]:
    def __init__(self, repository: R) -> None:
        self.repository = repository

    async def validate_id_exist(self, id_: UUID) -> M:
        model_object = await self.repository.get(id_)
        if model_object is None:
            raise APIException(
                http_status_code=status.HTTP_404_NOT_FOUND,
                error_code=ExceptionCode.NOT_FOUND,
            )
        return model_object

    async def delete(self, id_: UUID) -> None:
        model_object = await self.validate_id_exist(id_)
        await self.repository.delete(model_object)

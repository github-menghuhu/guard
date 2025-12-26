from collections.abc import AsyncGenerator

from api_exception import APIException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from guard.core.db import async_session_maker
from guard.core.exception import ExceptionCode


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    except ConnectionRefusedError:
        raise APIException(
            http_status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code=ExceptionCode.DB_CONNECTION_TIMEOUT,
        )

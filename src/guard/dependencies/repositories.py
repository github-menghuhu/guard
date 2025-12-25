from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from guard.dependencies import get_async_session
from guard.repositories import ClientRepository

"""

    repository层依赖注入工厂函数
    
"""


async def get_client_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> ClientRepository:
    return ClientRepository(db)

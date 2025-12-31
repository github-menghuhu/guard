from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from guard.dependencies import get_async_session
from guard.repositories import (
    ClientRepository,
    PermissionRepository,
    RoleRepository,
    UserRepository,
    OAuthProviderRepository,
)

"""

    repository层依赖注入工厂函数
    
"""


async def get_client_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> ClientRepository:
    return ClientRepository(db)


async def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserRepository:
    return UserRepository(db)


async def get_role_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> RoleRepository:
    return RoleRepository(db)


async def get_permission_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> PermissionRepository:
    return PermissionRepository(db)

async def get_oauth_provider_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> OAuthProviderRepository:
    return OAuthProviderRepository(db)

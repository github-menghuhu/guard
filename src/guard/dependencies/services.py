from typing import Annotated

from fastapi import Depends

from guard.core.crypto import password_hasher
from guard.dependencies import (
    get_client_repository,
    get_permission_repository,
    get_role_repository,
    get_user_repository,
    get_oauth_provider_repository,
)
from guard.repositories import (
    ClientRepository,
    PermissionRepository,
    RoleRepository,
    UserRepository,
    OAuthProviderRepository,
)
from guard.services import ClientService, PermissionService, RoleService, UserService, OAuthProviderService

"""

    service层依赖注入工厂函数

"""


async def get_client_service(
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)],
) -> ClientService:
    return ClientService(client_repository)


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository, password_hasher)


async def get_role_service(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> RoleService:
    return RoleService(role_repository)


async def get_permission_service(
    permission_repository: Annotated[
        PermissionRepository, Depends(get_permission_repository)
    ],
) -> PermissionService:
    return PermissionService(permission_repository)

async def get_oauth_provider_service(
    oauth_provider_repository: Annotated[
        OAuthProviderRepository, Depends(get_oauth_provider_repository)
    ],
) -> OAuthProviderService:
    return OAuthProviderService(oauth_provider_repository)

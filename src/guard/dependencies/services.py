from typing import Annotated

from fastapi import Depends

from guard.core.crypto import password_hasher
from guard.dependencies import get_client_repository, get_user_repository
from guard.repositories import ClientRepository, UserRepository
from guard.services import ClientService, UserService

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

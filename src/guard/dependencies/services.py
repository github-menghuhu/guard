from typing import Annotated

from fastapi import Depends

from guard.dependencies import get_client_repository
from guard.repositories import ClientRepository
from guard.services import ClientService

"""

    service层依赖注入工厂函数

"""


async def get_client_service(
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)],
) -> ClientService:
    return ClientService(client_repository)

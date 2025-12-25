from typing import Annotated

from api_exception import ResponseModel
from fastapi import APIRouter, Depends

from guard.dependencies import get_client_service
from guard.schemas import ClientResponse
from guard.services import ClientService

router = APIRouter(prefix="/client")


@router.post("/")
async def create_client(
    client_service: Annotated[ClientService, Depends(get_client_service)],
):
    client = await client_service.create(
        client_name="test-client",
        creator="mhh123",
        redirect_uris=[
            "http://localhost:8000/admin/auth/callback",
            "https://localhost:8000/admin/auth/callback",
        ],
    )

    return ResponseModel[ClientResponse](
        data=client,
        message="创建成功",
    )

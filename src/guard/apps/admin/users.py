from typing import Annotated
from uuid import UUID

from api_exception import ResponseModel
from fastapi import APIRouter, Depends, Path, Query

from guard.dependencies import get_client_service
from guard.schemas import ApiResponseDefaultMessage as ApiResponseMessage
from guard.schemas import (
    CreateClient,
    CreateClientParams,
    GetClient,
    ListClient,
    PaginationParams,
    UpdateClientParams,
)
from guard.services import ClientService

router = APIRouter(prefix="/user")


@router.post("/", name="user:create", response_model=ResponseModel[CreateUser])
async def create_user(
    create_params: CreateUserParams,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.create(
        client_name=create_params.client_name,
        redirect_uris=create_params.redirect_uris,
        creator="mhh1",
    )

    return ResponseModel[CreateUser](
        data=user,
        message=ApiResponseMessage.create_success,
    )

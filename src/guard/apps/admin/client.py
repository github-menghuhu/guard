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

router = APIRouter(prefix="/client")


@router.post("/", name="client:create")
async def create_client(
    create_params: CreateClientParams,
    client_service: Annotated[ClientService, Depends(get_client_service)],
):
    # client = await client_service.create(
    #     client_name="test-client",
    #     creator="mhh123",
    #     redirect_uris=[
    #         "http://localhost:8000/admin/auth/callback",
    #         "https://localhost:8000/admin/auth/callback",
    #     ],
    # )

    client = await client_service.create(
        client_name=create_params.client_name,
        redirect_uris=create_params.redirect_uris,
        creator=create_params.creator,
    )

    return ResponseModel[CreateClient](
        data=client,
        message=ApiResponseMessage.create_success,
    )


@router.get("/", name="client:list")
async def list_client(
    paginate: Annotated[PaginationParams, Depends()],
    client_service: Annotated[ClientService, Depends(get_client_service)],
    name: Annotated[str | None, Query(max_length=200)] = None,
    creator: Annotated[str | None, Query(max_length=200)] = None,
):
    clients = await client_service.list_paginate(
        name, creator, paginate.page, paginate.size
    )
    return ResponseModel[ListClient](
        data=clients,
        message=ApiResponseMessage.query_success,
    )


@router.get("/{id}", name="client:get")
async def get_client(
    id_: Annotated[UUID, Path(alias="id")],
    client_service: Annotated[ClientService, Depends(get_client_service)],
):
    client = await client_service.get(id_)
    return ResponseModel[GetClient](
        data=client,
        message=ApiResponseMessage.query_success,
    )


@router.patch("/{id}", name="client:update")
async def update_client(
    id_: Annotated[UUID, Path(alias="id")],
    update_params: UpdateClientParams,
    client_service: Annotated[ClientService, Depends(get_client_service)],
):
    client = await client_service.update(
        id_,
        update_params.name,
        update_params.redirect_uris,
        update_params.authorization_code_lifetime_seconds,
        update_params.access_id_token_lifetime_seconds,
        update_params.refresh_token_lifetime_seconds,
    )
    return ResponseModel[GetClient](
        data=client,
        message=ApiResponseMessage.update_success,
    )


@router.delete("/{id}", name="client:delete")
async def delete_client(
    id_: Annotated[UUID, Path(alias="id")],
    client_service: Annotated[ClientService, Depends(get_client_service)],
):
    await client_service.delete(id_)
    return ResponseModel(
        message=ApiResponseMessage.delete_success,
    )

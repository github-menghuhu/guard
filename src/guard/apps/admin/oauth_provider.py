from typing import Annotated
from uuid import UUID

from api_exception import ResponseModel
from fastapi import APIRouter, Depends, Path, Query

from guard.dependencies import get_oauth_provider_service
from guard.schemas import ApiResponseDefaultMessage as ApiResponseMessage
from guard.schemas import (
    CreateOAuthProvider,
    CreateOAuthProviderParams,
    GetOAuthProvider,
    ListOAuthProvider,
    PaginationParams,
    UpdateOAuthProviderParams,
)
from guard.services import OAuthProviderService

router = APIRouter(prefix="/oauth_provider")


@router.post("/", name="oauth_provider:create", response_model=ResponseModel[CreateOAuthProvider])
async def create_oauth_provider(
    create_params: CreateOAuthProviderParams,
    oauth_provider_service: Annotated[OAuthProviderService, Depends(get_oauth_provider_service)],
):
    oauth_provider = await oauth_provider_service.create(create_params.name, create_params.client_id, create_params.client_secret, create_params.scopes)
    return ResponseModel[CreateOAuthProvider](
        data=oauth_provider,
        message=ApiResponseMessage.create_success,
    )


@router.get("/", name="oauth_provider:list", response_model=ResponseModel[ListOAuthProvider])
async def list_oauth_provider(
    paginate: Annotated[PaginationParams, Depends()],
    oauth_provider_service: Annotated[OAuthProviderService, Depends(get_oauth_provider_service)],
    name: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
):
    oauth_providers = await oauth_provider_service.list_paginate(
        name, paginate.page, paginate.size
    )
    return ResponseModel[ListOAuthProvider](
        data=oauth_providers,
        message=ApiResponseMessage.query_success,
    )


@router.get("/{id}", name="oauth_provider:get", response_model=ResponseModel[GetOAuthProvider])
async def get_oauth_provider(
    id_: Annotated[UUID, Path(alias="id")],
    oauth_provider_service: Annotated[OAuthProviderService, Depends(get_oauth_provider_service)],
):
    oauth_provider = await oauth_provider_service.get(id_)
    return ResponseModel[GetOAuthProvider](
        data=oauth_provider,
        message=ApiResponseMessage.query_success,
    )


@router.patch("/{id}", name="oauth_provider:update", response_model=ResponseModel[GetOAuthProvider])
async def update_oauth_provider(
    id_: Annotated[UUID, Path(alias="id")],
    update_params: UpdateOAuthProviderParams,
    oauth_provider_service: Annotated[OAuthProviderService, Depends(get_oauth_provider_service)],
):
    oauth_provider = await oauth_provider_service.update(id_, update_params.name, update_params.client_id, update_params.client_secret, update_params.scopes)
    return ResponseModel[GetOAuthProvider](
        data=oauth_provider,
        message=ApiResponseMessage.update_success,
    )


@router.delete("/{id}", name="oauth_provider:delete", response_model=ResponseModel)
async def delete_oauth_provider(
    id_: Annotated[UUID, Path(alias="id")],
    oauth_provider_service: Annotated[OAuthProviderService, Depends(get_oauth_provider_service)],
):
    await oauth_provider_service.delete(id_)
    return ResponseModel(
        message=ApiResponseMessage.delete_success,
    )

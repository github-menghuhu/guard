from typing import Annotated
from uuid import UUID

from api_exception import ResponseModel
from fastapi import APIRouter, Depends, Path, Query

from guard.dependencies import get_permission_service
from guard.schemas import ApiResponseDefaultMessage as ApiResponseMessage
from guard.schemas import (
    CreatePermission,
    CreatePermissionParams,
    GetPermission,
    ListPermission,
    PaginationParams,
    UpdatePermissionParams,
)
from guard.services import PermissionService

router = APIRouter(prefix="/permission")


@router.post(
    "/", name="permission:create", response_model=ResponseModel[CreatePermission]
)
async def create_permission(
    create_params: CreatePermissionParams,
    permission_service: Annotated[PermissionService, Depends(get_permission_service)],
):
    permission = await permission_service.create(create_params.name, create_params.code)
    return ResponseModel[CreatePermission](
        data=permission,
        message=ApiResponseMessage.create_success,
    )


@router.get("/", name="permission:list", response_model=ResponseModel[ListPermission])
async def list_permission(
    paginate: Annotated[PaginationParams, Depends()],
    permission_service: Annotated[PermissionService, Depends(get_permission_service)],
    name: Annotated[str | None, Query(min_length=1, max_length=200)] = None,
    code: Annotated[str | None, Query(min_length=1, max_length=200)] = None,
):
    permissions = await permission_service.list_paginate(
        name, code, paginate.page, paginate.size
    )
    return ResponseModel[ListPermission](
        data=permissions,
        message=ApiResponseMessage.query_success,
    )


@router.get("/{id}", name="permission:get", response_model=ResponseModel[GetPermission])
async def get_permission(
    id_: Annotated[UUID, Path(alias="id")],
    permission_service: Annotated[PermissionService, Depends(get_permission_service)],
):
    permission = await permission_service.get(id_)
    return ResponseModel[GetPermission](
        data=permission,
        message=ApiResponseMessage.query_success,
    )


@router.patch(
    "/{id}", name="permission:update", response_model=ResponseModel[GetPermission]
)
async def update_permission(
    id_: Annotated[UUID, Path(alias="id")],
    update_params: UpdatePermissionParams,
    permission_service: Annotated[PermissionService, Depends(get_permission_service)],
):
    permission = await permission_service.update(
        id_, update_params.name, update_params.code
    )
    return ResponseModel[GetPermission](
        data=permission,
        message=ApiResponseMessage.update_success,
    )


@router.delete("/{id}", name="permission:delete", response_model=ResponseModel)
async def delete_permission(
    id_: Annotated[UUID, Path(alias="id")],
    permission_service: Annotated[PermissionService, Depends(get_permission_service)],
):
    await permission_service.delete(id_)
    return ResponseModel(
        message=ApiResponseMessage.delete_success,
    )

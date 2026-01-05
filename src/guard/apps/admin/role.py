from typing import Annotated
from uuid import UUID

from api_exception import ResponseModel
from fastapi import APIRouter, Depends, Path, Query

from guard.dependencies import get_role_service
from guard.schemas import ApiResponseDefaultMessage as ApiResponseMessage
from guard.schemas import (
    CreateRole,
    CreateRoleParams,
    GetRole,
    ListRole,
    PaginationParams,
    UpdateRoleParams,
)
from guard.services import RoleService

router = APIRouter(prefix="/role")


@router.post(
    "/",
    name="role:create",
    response_model=ResponseModel[CreateRole],
    description="创建角色",
)
async def create_role(
    create_params: CreateRoleParams,
    role_service: Annotated[RoleService, Depends(get_role_service)],
):
    role = await role_service.create(create_params.name, create_params.default)
    return ResponseModel[CreateRole](
        data=role,
        message=ApiResponseMessage.create_success,
    )


@router.get(
    "/",
    name="role:list",
    response_model=ResponseModel[ListRole],
    description="查询角色列表",
)
async def list_role(
    paginate: Annotated[PaginationParams, Depends()],
    role_service: Annotated[RoleService, Depends(get_role_service)],
    name: Annotated[
        str | None,
        Query(min_length=1, max_length=200, description="角色名称，支持模糊匹配"),
    ] = None,
    default: Annotated[bool | None, Query(description="是否为基础用户默认角色")] = None,
):
    roles = await role_service.list_paginate(
        name, default, paginate.page, paginate.size
    )
    return ResponseModel[ListRole](
        data=roles,
        message=ApiResponseMessage.query_success,
    )


@router.get(
    "/{id}",
    name="role:get",
    response_model=ResponseModel[GetRole],
    description="查询角色详情",
)
async def get_role(
    id_: Annotated[UUID, Path(alias="id", description="角色ID")],
    role_service: Annotated[RoleService, Depends(get_role_service)],
):
    role = await role_service.get(id_)
    return ResponseModel[GetRole](
        data=role,
        message=ApiResponseMessage.query_success,
    )


@router.patch(
    "/{id}",
    name="role:update",
    response_model=ResponseModel[GetRole],
    description="更新角色信息",
)
async def update_role(
    id_: Annotated[UUID, Path(alias="id", description="角色ID")],
    update_params: UpdateRoleParams,
    role_service: Annotated[RoleService, Depends(get_role_service)],
):
    role = await role_service.update(id_, update_params.name, update_params.default)
    return ResponseModel[GetRole](
        data=role,
        message=ApiResponseMessage.update_success,
    )


@router.delete(
    "/{id}", name="role:delete", response_model=ResponseModel, description="删除角色"
)
async def delete_role(
    id_: Annotated[UUID, Path(alias="id", description="角色ID")],
    role_service: Annotated[RoleService, Depends(get_role_service)],
):
    await role_service.delete(id_)
    return ResponseModel(
        message=ApiResponseMessage.delete_success,
    )

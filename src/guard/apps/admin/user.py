from typing import Annotated
from uuid import UUID

from api_exception import ResponseModel
from fastapi import APIRouter, Depends, Path, Query

from guard.dependencies import get_user_service
from guard.schemas import ApiResponseDefaultMessage as ApiResponseMessage
from guard.schemas import (
    CreateUser,
    CreateUserParams,
    GetUser,
    ListUser,
    PaginationParams,
    UpdateUser,
    UpdateUserParams,
)
from guard.services import UserService

router = APIRouter(prefix="/user")


@router.post("/", name="user:create", response_model=ResponseModel[CreateUser])
async def create_user(
    create_params: CreateUserParams,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.create(
        email=create_params.email,
        password=create_params.password,
    )

    return ResponseModel[CreateUser](
        data=user,
        message=ApiResponseMessage.create_success,
    )


@router.get(
    "/",
    name="user:list",
    response_model=ResponseModel[ListUser],
    description="查询用户列表",
)
async def list_user(
    paginate: Annotated[PaginationParams, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    name: Annotated[
        str | None,
        Query(min_length=1, max_length=200, description="用户名，支持模糊匹配"),
    ] = None,
    email: Annotated[
        str | None,
        Query(min_length=1, max_length=300, description="邮箱，支持模糊匹配"),
    ] = None,
    phone: Annotated[
        str | None,
        Query(min_length=3, max_length=11, description="手机号，支持模糊匹配"),
    ] = None,
):
    users = await user_service.list_paginate(
        name, email, phone, paginate.page, paginate.size
    )
    return ResponseModel[ListUser](
        data=users,
        message=ApiResponseMessage.query_success,
    )


@router.get(
    "/{id}",
    name="user:get",
    response_model=ResponseModel[GetUser],
    description="查询用户详情",
)
async def get_user(
    id_: Annotated[UUID, Path(alias="id", description="用户ID")],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.get(id_)
    return ResponseModel[GetUser](
        data=user,
        message=ApiResponseMessage.query_success,
    )


@router.patch(
    "/{id}",
    name="user:update",
    response_model=ResponseModel[UpdateUser],
    description="更新用户信息",
)
async def update_user(
    id_: Annotated[UUID, Path(alias="id", description="用户ID")],
    update_params: UpdateUserParams,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.update(
        id_,
        update_params.name,
        update_params.is_active,
    )
    return ResponseModel[UpdateUser](
        data=user,
        message=ApiResponseMessage.update_success,
    )


@router.delete(
    "/{id}", name="user:delete", response_model=ResponseModel, description="删除用户"
)
async def delete_user(
    id_: Annotated[UUID, Path(alias="id", description="用户ID")],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    await user_service.delete(id_)
    return ResponseModel(
        message=ApiResponseMessage.delete_success,
    )

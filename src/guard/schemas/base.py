from enum import StrEnum
from typing import Annotated, TypeVar

from fastapi import Query
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from sqlalchemy.orm import DeclarativeBase

M = TypeVar("M", bound=DeclarativeBase)


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class ApiResponseDefaultMessage(StrEnum):
    create_success = "Create Success."
    update_success = "Update Success."
    delete_success = "Delete Success."
    query_success = "Query Success."


class Paginate[M](BaseModel):
    total: int = 0
    page: int = 1
    size: int = 10
    items: list[M]


class PaginationParams:
    def __init__(
        self,
        page: Annotated[int, Query(ge=1)] = 1,
        size: Annotated[int, Query(ge=10, le=50)] = 10,
    ):
        self.page = page
        self.size = size

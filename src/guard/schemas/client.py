from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from guard.models import GrantTypes, ResponseTypes, Scopes
from guard.schemas import BaseModel, Paginate


class CreateClientParams(BaseModel):
    client_name: Annotated[str, Field(min_length=1, max_length=255)]
    redirect_uris: Annotated[list[str], Field(min_length=1)]
    grant_types: Annotated[list[GrantTypes], Field(min_length=1)] = [
        GrantTypes.AUTHORIZATION_CODE
    ]
    response_types: Annotated[list[ResponseTypes], Field(min_length=1)] = [
        ResponseTypes.CODE
    ]
    scopes: Annotated[list[Scopes], Field(min_length=1)] = [Scopes.OPENID]


class UpdateClientParams(BaseModel):
    client_name: Annotated[str | None, Field(min_length=1, max_length=255)] = None
    redirect_uris: Annotated[list[str] | None, Field(min_length=1)] = None
    grant_types: Annotated[list[GrantTypes] | None, Field(min_length=1)] = None
    response_types: Annotated[list[ResponseTypes] | None, Field(min_length=1)] = None
    scopes: Annotated[list[Scopes] | None, Field(min_length=1)] = None
    authorization_code_lifetime_seconds: Annotated[int | None, Field(ge=60)] = None
    access_id_token_lifetime_seconds: Annotated[int | None, Field(ge=60)] = None
    refresh_token_lifetime_seconds: Annotated[int | None, Field(ge=120)] = None


class _ClientBase(BaseModel):
    id: UUID
    client_id: str
    client_name: str
    client_secret: str
    redirect_uris: list[str]
    creator: str
    created_at: datetime
    grant_types: list[str]
    response_types: list[str]
    scopes: list[str]
    authorization_code_lifetime_seconds: int
    access_id_token_lifetime_seconds: int
    refresh_token_lifetime_seconds: int


class CreateClient(_ClientBase):
    pass


class GetClient(_ClientBase):
    pass


class ListClient(Paginate):
    items: list[GetClient]


class UpdateClient(GetClient):
    updated_at: datetime

from datetime import datetime
from uuid import UUID

from guard.models import GrantTypes, ResponseTypes, Scopes
from guard.schemas import BaseModel


class CreateClientParams(BaseModel):
    client_name: str
    redirect_uris: list[str]
    grant_types: list[GrantTypes] = [GrantTypes.AUTHORIZATION_CODE]
    response_types: list[ResponseTypes] = [ResponseTypes.CODE]
    scopes: list[Scopes] = [Scopes.OPENID]


class UpdateClientParams(BaseModel):
    name: str | None = None
    redirect_uris: list[str] | None = None
    grant_types: list[GrantTypes] | None = None
    response_types: list[ResponseTypes] | None = None
    scopes: list[Scopes] | None = None
    authorization_code_lifetime_seconds: int | None = None
    access_id_token_lifetime_seconds: int | None = None
    refresh_token_lifetime_seconds: int | None = None


class ClientBase(BaseModel):
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


class CreateClient(ClientBase):
    pass


class GetClient(ClientBase):
    pass


class ListClient(BaseModel):
    total: int
    page: int
    size: int
    items: list[GetClient]


class UpdateClient(GetClient):
    updated_at: datetime

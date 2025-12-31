from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from guard.schemas import BaseModel, Paginate


class CreateOAuthProviderParams(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50, description="名称")]
    client_id: Annotated[str, Field(min_length=1,description="客户端ID")]
    client_secret: Annotated[str, Field(min_length=1,description="客户端密钥")]
    scopes: Annotated[list[str], Field(min_length=1, description="授权范围")]


class UpdateOAuthProviderParams(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=50, description="名称")] = None
    client_id: Annotated[str | None, Field(min_length=1, description="客户端ID")] = None
    client_secret: Annotated[str | None, Field(min_length=1, description="客户端密钥")] = None
    scopes: Annotated[list[str] | None, Field(min_length=1, description="授权范围")] = None


class _OAuthProviderBase(BaseModel):
    id: UUID
    name: str
    client_id: str
    client_secret: str
    scopes: list[str]
    created_at: datetime


class CreateOAuthProvider(_OAuthProviderBase):
    pass


class GetOAuthProvider(_OAuthProviderBase):
    pass


class ListOAuthProvider(Paginate):
    items: list[GetOAuthProvider]


class UpdateOAuthProvider(GetOAuthProvider):
    updated_at: datetime

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from guard.models import GrantTypes, ResponseTypes, Scopes
from guard.schemas import BaseModel, Paginate


class AuthorizeParams(BaseModel):
    client_name: Annotated[str, Field(min_length=1, max_length=255)]
    redirect_uris: Annotated[list[str], Field(min_length=1)]
    grant_types: Annotated[list[GrantTypes], Field(min_length=1)] = [
        GrantTypes.AUTHORIZATION_CODE
    ]
    response_types: Annotated[list[ResponseTypes], Field(min_length=1)] = [
        ResponseTypes.CODE
    ]
    scopes: Annotated[list[Scopes], Field(min_length=1)] = [Scopes.OPENID]
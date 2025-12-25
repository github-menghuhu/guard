from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ClientResponse(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)

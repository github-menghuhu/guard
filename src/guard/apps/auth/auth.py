from typing import Annotated

from api_exception import ResponseModel
from fastapi import APIRouter, Depends

from guard.models import Client
from guard.repositories import ClientRepository

router = APIRouter()


# @router.get("/authorize", tags=["auth"])
# async def authorize(
#     response_type: Annotated[ResponseTypes, Query()] = ResponseTypes.CODE,
#     client_id: Annotated[str, Query()] = "",
#     redirect_uri: Annotated[str, Query()] = "",
#     scope: Annotated[str, Query()] = "",
#     response_mode: Annotated[str, Query()] = "",
#     prompt: Annotated[str, Query()] = "",
#     screen: Annotated[str, Query()] = "",
#     code_challenge: str | None = Query(None),
#     code_challenge_method: str | None = Query("plain"),
#     nonce: Annotated[str, Query()] = "",
#     state: Annotated[str, Query()] = "",
#     requested_acr: Annotated[str, Query()] = "",
# ):
#     pass


@router.get("/authorize", tags=["auth"])
async def authorize(
    client_repository: Annotated[ClientRepository, Depends()],
):
    client = Client(
        client_name="test-client",
        redirect_uris=[
            "http://localhost:8000/admin/auth/callback",
            "https://localhost:8000/admin/auth/callback",
        ],
        creator="mhh",
    )
    a = await client_repository.create(client)
    return ResponseModel[dict](
        data={
            "id": a.id,
            "client_id": a.client_id,
            "client_name": a.client_name,
            "client_secret": a.client_secret,
            "redirect_uris": a.redirect_uris,
            "creator": a.creator,
            "created_at": a.created_at,
            "updated_at": a.updated_at,
            "grant_types": a.grant_types,
            "response_types": a.response_types,
            "scopes": a.scopes,
            "authorization_code_lifetime_seconds": a.authorization_code_lifetime_seconds,
            "access_id_token_lifetime_seconds": a.access_id_token_lifetime_seconds,
            "refresh_token_lifetime_seconds": a.refresh_token_lifetime_seconds,
            "encrypt_jwk": a.encrypt_jwk,
        },
        message="创建成功",
    )

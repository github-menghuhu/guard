from typing import Annotated
from uuid import UUID

from api_exception import ResponseModel
from fastapi import APIRouter, Depends, Path, Query

from guard.models import GrantTypes, ResponseTypes, Scopes, ResponseMode, Prompt, ACR

router = APIRouter(prefix="/auth")


@router.get("/authorize", name="client:create")
async def authorize(
        redirect_uri: Annotated[list[str], Query(min_length=1)],
        client_id: str,
        response_type: ResponseTypes = ResponseTypes.CODE,
        scope: Scopes = Scopes.OPENID,
        response_mode: ResponseMode = ResponseMode.QUERY,
        prompt: Prompt | None = Prompt.NONE,
        code_challenge: str | None = None,
        nonce: str | None = None,
        state: str | None = None,
        requested_acr: ACR = ACR.LEVEL_0,
):
    pass
    return {"message": "ok"}

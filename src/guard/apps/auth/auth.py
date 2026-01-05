from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import HttpUrl

from guard.models import Prompt, ResponseMode, ResponseTypes, Scopes

router = APIRouter(prefix="/auth")


@router.get("/authorize", name="auth:authorize")
async def authorize(
    client_id: Annotated[UUID, Query(description="客户端ID")],
    redirect_uri: Annotated[HttpUrl, Query(description="回调地址")],
    code_challenge: Annotated[
        str, Query(min_length=43, max_length=128, description="PKCE挑战字符串")
    ],
    response_type: Annotated[
        ResponseTypes, Query(description="响应类型")
    ] = ResponseTypes.CODE,
    scope: Annotated[Scopes, Query(description="授权范围")] = Scopes.OPENID,
    response_mode: Annotated[
        ResponseMode, Query(description="响应模式")
    ] = ResponseMode.QUERY,
    prompt: Annotated[
        Prompt, Query(description="指定认证服务器与终端用户的交互方式")
    ] = Prompt.LOGIN,
    nonce: Annotated[
        str | None,
        Query(
            min_length=16, max_length=64, description="随机字符串，用于防范Replay攻击"
        ),
    ] = None,
    state: Annotated[
        str | None,
        Query(
            min_length=16, max_length=128, description="随机字符串，用于防范CSRF攻击"
        ),
    ] = None,
):
    pass

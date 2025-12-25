from fastapi import APIRouter

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

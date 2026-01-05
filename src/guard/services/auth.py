from uuid import UUID

from api_exception import APIException
from fastapi import status
from pydantic import HttpUrl

from guard.core.exception import ExceptionCode
from guard.models import (
    Client,
    Prompt,
    ResponseMode,
    ResponseTypes,
    Scopes,
)
from guard.repositories import (
    AuthorizationCodeRepository,
    ClientRepository,
)


class AuthService:
    def __init__(
        self,
        client_repository: ClientRepository,
        authorization_code_repository: AuthorizationCodeRepository,
    ) -> None:
        self.client_repository = client_repository
        self.authorization_code_repository = authorization_code_repository

    def _validate_client_configuration(
        self,
        client: Client,
        redirect_uri: HttpUrl | None = None,
        scope: Scopes | None = None,
        response_type: ResponseTypes | None = None,
    ) -> None:
        validations = {
            "redirect_uri": (redirect_uri, client.redirect_uris),
            "scope": (scope, client.scopes),
            "response_type": (response_type, client.response_types),
        }

        for prop_name, (value, allowed_values) in validations.items():
            if value is not None and value not in allowed_values:
                raise APIException(
                    http_status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    error_code=ExceptionCode.VALIDATION_ERROR,
                    message=f"{prop_name}:{value} is not in the allowed {prop_name}s list for this client",
                )

    async def authorize(
        self,
        client_id: UUID,
        redirect_uri: HttpUrl,
        response_type: ResponseTypes,
        scope: Scopes,
        response_mode: ResponseMode,
        prompt: Prompt,
        code_challenge: str,
        nonce: str | None = None,
        state: str | None = None,
        user=None,
    ):
        client = await self.client_repository.get(client_id)
        self._validate_client_configuration(client, redirect_uri, scope, response_type)

        if prompt == Prompt.LOGIN:
            redirect_to = "http://xxxxxxlogin"
        elif prompt == Prompt.CONSENT:
            if user is None:
                redirect_to = "http://xxxxxxlogin"

            redirect_to = "http://xxxxxxconsent"
        elif prompt == Prompt.NONE:
            if user is None:
                redirect_to = "http://xxxxxxlogin"

            redirect_to = "http://xxxxxxconsent"

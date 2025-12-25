from guard.models import Client, GrantTypes, ResponseTypes, Scopes
from guard.repositories import ClientRepository
from guard.schemas import ClientResponse


class ClientService:
    def __init__(self, client_repository: ClientRepository) -> None:
        self.client_repository = client_repository

    async def create(
        self,
        client_name: str,
        creator: str,
        redirect_uris: list[str] | None = None,
        grant_types: list[GrantTypes] | None = None,
        response_types: list[ResponseTypes] | None = None,
        scopes: list[Scopes] | None = None,
        authorization_code_lifetime_seconds: int | None = None,
        access_id_token_lifetime_seconds: int | None = None,
        refresh_token_lifetime_seconds: int | None = None,
        encrypt_jwk: str | None = None,
    ) -> ClientResponse:
        client = Client(client_name=client_name, creator=creator)

        if redirect_uris:
            client.redirect_uris = redirect_uris

        if grant_types:
            client.grant_types = [gt.value for gt in grant_types]

        if response_types:
            client.response_types = [rt.value for rt in response_types]

        if scopes:
            client.scopes = [s.value for s in scopes]

        if authorization_code_lifetime_seconds:
            client.authorization_code_lifetime_seconds = (
                authorization_code_lifetime_seconds
            )

        if access_id_token_lifetime_seconds:
            client.access_id_token_lifetime_seconds = access_id_token_lifetime_seconds

        if refresh_token_lifetime_seconds:
            client.refresh_token_lifetime_seconds = refresh_token_lifetime_seconds

        if encrypt_jwk:
            client.encrypt_jwk = encrypt_jwk

        client = await self.client_repository.create(client)
        return ClientResponse.model_validate(client)

from uuid import UUID

from guard.models import Client, GrantTypes, ResponseTypes, Scopes
from guard.repositories import ClientRepository
from guard.schemas import CreateClient, GetClient, ListClient, UpdateClient
from guard.services.base import BaseService


class ClientService(BaseService[ClientRepository, Client]):
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
    ) -> CreateClient:
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

        client = await self.repository.create(client)
        return CreateClient.model_validate(client)

    async def list_paginate(
        self,
        name: str | None = None,
        creator: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> ListClient:
        items = await self.repository.list_paginate(name, creator, page, size)
        return ListClient.model_validate(items)

    async def get(self, id_: UUID) -> GetClient:
        client = await self.validate_id_exist(id_)
        return GetClient.model_validate(client)

    async def update(
        self,
        id_: UUID,
        client_name: str | None = None,
        redirect_uris: list[str] | None = None,
        authorization_code_lifetime_seconds: int | None = None,
        access_id_token_lifetime_seconds: int | None = None,
        refresh_token_lifetime_seconds: int | None = None,
    ) -> UpdateClient:
        client = await self.validate_id_exist(id_)

        if client_name:
            client.client_name = client_name

        if redirect_uris:
            client.redirect_uris = redirect_uris

        if authorization_code_lifetime_seconds:
            client.authorization_code_lifetime_seconds = (
                authorization_code_lifetime_seconds
            )

        if access_id_token_lifetime_seconds:
            client.access_id_token_lifetime_seconds = access_id_token_lifetime_seconds

        if refresh_token_lifetime_seconds:
            client.refresh_token_lifetime_seconds = refresh_token_lifetime_seconds

        client = await self.repository.update(client)
        return UpdateClient.model_validate(client)

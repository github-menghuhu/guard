from uuid import UUID

from guard.models import OAuthProvider
from guard.repositories import OAuthProviderRepository
from guard.schemas import CreateOAuthProvider, GetOAuthProvider, ListOAuthProvider, UpdateOAuthProvider
from guard.services.base import BaseService


class OAuthProviderService(BaseService[OAuthProviderRepository, OAuthProvider]):
    async def create(
            self, name: str, client_id: str, client_secret: str, scopes: list[str]
    ) -> CreateOAuthProvider:
        oauth_provider = OAuthProvider(name=name, client_id=client_id, client_secret=client_secret, scopes=scopes)
        oauth_provider = await self.repository.create(oauth_provider)
        return CreateOAuthProvider.model_validate(oauth_provider)

    async def list_paginate(
            self,
            name: str | None = None,
            page: int = 1,
            size: int = 10,
    ) -> ListOAuthProvider:
        items = await self.repository.list_paginate(name, page, size)
        return ListOAuthProvider.model_validate(items)

    async def get(self, id_: UUID) -> GetOAuthProvider:
        oauth_provider = await self.validate_id_exist(id_)
        return GetOAuthProvider.model_validate(oauth_provider)

    async def update(
            self,
            id_: UUID,
            name: str | None = None,
            client_id: str | None = None,
            client_secret: str | None = None,
            scopes: list[str] | None = None
    ) -> UpdateOAuthProvider:
        oauth_provider = await self.validate_id_exist(id_)

        if name:
            oauth_provider.name = name

        if client_id:
            oauth_provider.client_id = client_id

        if client_secret:
            oauth_provider.client_secret = client_secret

        if scopes:
            oauth_provider.scopes = scopes

        oauth_provider = await self.repository.update(oauth_provider)
        return UpdateOAuthProvider.model_validate(oauth_provider)

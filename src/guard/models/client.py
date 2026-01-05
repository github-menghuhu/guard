import secrets

from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from guard.core.config import settings
from guard.models.base import (
    Base,
    CreatedUpdatedAtMixin,
    Scopes,
    UUIDPrimaryKeyMixin,
    generate_client_default_grant_types,
    generate_client_default_response_types,
)


class Client(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "clients"

    client_name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    client_id: Mapped[str] = mapped_column(
        String(length=255), default=secrets.token_urlsafe, nullable=False, index=True
    )
    client_secret: Mapped[str] = mapped_column(
        String(length=255), default=secrets.token_urlsafe, nullable=False, index=True
    )
    redirect_uris: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])
    grant_types: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=generate_client_default_grant_types
    )
    response_types: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=generate_client_default_response_types
    )
    scopes: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=[Scopes.OPENID]
    )
    authorization_code_lifetime_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=settings.DEFAULT_AUTHORIZATION_CODE_LIFETIME_SECONDS,
    )
    access_id_token_lifetime_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=settings.DEFAULT_ACCESS_ID_TOKEN_LIFETIME_SECONDS,
    )
    refresh_token_lifetime_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=settings.DEFAULT_REFRESH_TOKEN_LIFETIME_SECONDS
    )
    encrypt_jwk: Mapped[str | None] = mapped_column(Text, nullable=True)
    creator: Mapped[str] = mapped_column(String(length=255), nullable=False)

import secrets
import uuid
from enum import StrEnum

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guard.core.config import settings
from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
)
from guard.models.tenant import Tenant


class GrantTypes(StrEnum):
    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"


def generate_client_default_grant_types() -> list[str]:
    return [gt.value for gt in GrantTypes]


class ResponseTypes(StrEnum):
    CODE = "code"
    CODE_ID_TOKEN = "code id_token"
    CODE_TOKEN = "code token"
    CODE_ID_TOKEN_TOKEN = "code id_token token"


def generate_client_default_response_types() -> list[str]:
    return [rt.value for rt in ResponseTypes]


class Client(Base, CreatedUpdatedAtMixin):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
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
    scopes: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=["openid"])
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

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Tenant.id, ondelete="CASCADE")
    )
    tenant: Mapped[Tenant] = relationship(back_populates="clients")

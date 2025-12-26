from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from guard.models.base import (
    Base,
    CreatedUpdatedAtMixin,
    EncryptedString,
    UUIDPrimaryKeyMixin,
)


class OAuthProvider(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "oauth_providers"

    provider_name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    client_id: Mapped[str] = mapped_column(EncryptedString, nullable=False)
    client_secret: Mapped[str] = mapped_column(EncryptedString, nullable=False)
    scopes: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

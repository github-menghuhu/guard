import secrets
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guard.core.config import settings
from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    ExpiresAtMixin,
    UUIDPrimaryKeyMixin,
)
from guard.models.oauth_account import OAuthAccount
from guard.models.oauth_provider import OAuthProvider


class OAuthSession(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, ExpiresAtMixin, Base):
    __tablename__ = "oauth_sessions"
    __lifetime_seconds = settings.OAUTH_SESSION_LIFETIME_SECONDS

    token: Mapped[str] = mapped_column(
        String(length=255),
        default=secrets.token_urlsafe,
        nullable=False,
        index=True,
        unique=True,
    )
    redirect_uri: Mapped[str] = mapped_column(Text, nullable=False)

    oauth_provider_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(OAuthProvider.id, ondelete="CASCADE"), nullable=False
    )
    oauth_provider: Mapped[OAuthProvider] = relationship()

    oauth_account_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID, ForeignKey(OAuthAccount.id, ondelete="CASCADE"), nullable=True
    )
    oauth_account: Mapped[OAuthAccount | None] = relationship()

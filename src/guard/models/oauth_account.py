import uuid
from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import UniqueConstraint

from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    EncryptedString,
    UTCDateTime,
)
from guard.models.oauth_provider import OAuthProvider
from guard.models.tenant import Tenant
from guard.models.user import User


class OAuthAccount(Base, CreatedUpdatedAtMixin):
    __tablename__ = "oauth_accounts"
    __table_args__ = (
        UniqueConstraint("oauth_provider_id", "user_id"),
        UniqueConstraint("oauth_provider_id", "account_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    account_id: Mapped[str] = mapped_column(
        String(length=512), index=True, nullable=False
    )
    account_email: Mapped[str | None] = mapped_column(String(length=512), nullable=True)
    access_token: Mapped[str] = mapped_column(EncryptedString, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(
        UTCDateTime(timezone=True), nullable=True
    )
    refresh_token: Mapped[str | None] = mapped_column(EncryptedString, nullable=True)

    oauth_provider_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(OAuthProvider.id, ondelete="CASCADE"), nullable=False
    )
    oauth_provider: Mapped[OAuthProvider] = relationship()

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=True
    )
    user: Mapped[User | None] = relationship()

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(Tenant.id, ondelete="CASCADE"), nullable=False
    )
    tenant: Mapped[Tenant] = relationship()

    def is_expired(self) -> bool:
        return self.expires_at is not None and self.expires_at < datetime.now(UTC)

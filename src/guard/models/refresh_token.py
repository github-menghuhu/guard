import uuid
from datetime import datetime

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    ExpiresAtMixin,
    UTCDateTime,
    UUIDPrimaryKeyMixin,
)
from guard.models.client import Client
from guard.models.user import User


class RefreshToken(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, ExpiresAtMixin, Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
        index=True,
        unique=True,
    )
    scope: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    authenticated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(timezone=True), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship()

    client_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(Client.id, ondelete="CASCADE"), nullable=False
    )
    client: Mapped[Client] = relationship()

import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guard.core.config import settings
from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    ExpiresAtMixin,
    Scopes,
    UUIDPrimaryKeyMixin,
)
from guard.models.client import Client
from guard.models.user import User


class IDToken(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, ExpiresAtMixin, Base):
    __tablename__ = "id_tokens"
    __lifetime_seconds__ = settings.DEFAULT_ACCESS_ID_TOKEN_LIFETIME_SECONDS

    token: Mapped[str] = mapped_column(
        String(length=255), nullable=False, index=True, unique=True
    )
    scope: Mapped[list[Scopes]] = mapped_column(JSON, nullable=False, default=list)

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship()

    client_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(Client.id, ondelete="CASCADE"), nullable=False
    )
    client: Mapped[Client] = relationship()

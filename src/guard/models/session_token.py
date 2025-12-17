import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guard.core.config import settings
from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    ExpiresAtMixin,
)
from guard.models.user import User


class SessionToken(Base, CreatedUpdatedAtMixin, ExpiresAtMixin):
    __tablename__ = "session_tokens"
    __lifetime_seconds__ = settings.SESSION_LIFETIME_SECONDS

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column(
        String(length=255), nullable=False, index=True, unique=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship()

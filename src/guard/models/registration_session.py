import secrets
import uuid
from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from guard.core.config import settings
from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    ExpiresAtMixin,
)
from guard.models.oauth_account import OAuthAccount


class RegistrationSessionFlow(StrEnum):
    PASSWORD = "PASSWORD"
    OAUTH = "OAUTH"


class RegistrationSession(Base, CreatedUpdatedAtMixin, ExpiresAtMixin):
    __tablename__ = "registration_sessions"
    __lifetime_seconds = settings.REGISTRATION_SESSION_LIFETIME_SECONDS

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column(
        String(length=255),
        default=secrets.token_urlsafe,
        nullable=False,
        index=True,
        unique=True,
    )
    flow: Mapped[RegistrationSessionFlow] = mapped_column(
        String(length=255), default=RegistrationSessionFlow.PASSWORD, nullable=False
    )
    email: Mapped[str | None] = mapped_column(String(length=320), nullable=True)

    oauth_account_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID, ForeignKey(OAuthAccount.id, ondelete="CASCADE"), nullable=True
    )
    oauth_account: Mapped[OAuthAccount | None] = relationship()

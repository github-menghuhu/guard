import uuid
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import JSON, String

from guard.models.base import (
    GUID,
    TABLE_PREFIX,
    Base,
    CreatedUpdatedAtMixin,
    ExpiresAtMixin,
    UTCDateTime,
)
from guard.models.client import Client
from guard.models.login_session import ACR
from guard.models.user import User


class AuthorizationCode(Base, CreatedUpdatedAtMixin, ExpiresAtMixin):
    __tablename__ = "authorization_codes"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(
        String(length=255), nullable=False, index=True, unique=True
    )
    c_hash: Mapped[str] = mapped_column(String(length=255), nullable=False)
    redirect_uri: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    authenticated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(timezone=True), nullable=False
    )
    nonce: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    acr: Mapped[ACR] = mapped_column(
        Enum(ACR, name=f"{TABLE_PREFIX}acr"), nullable=False, default=ACR.LEVEL_0
    )
    code_challenge: Mapped[str | None] = mapped_column(
        String(length=255), nullable=True
    )
    code_challenge_method: Mapped[str | None] = mapped_column(
        String(length=255), nullable=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship()

    client_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(Client.id, ondelete="CASCADE"), nullable=False
    )
    client: Mapped[Client] = relationship()

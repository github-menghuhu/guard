import secrets
import uuid
from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import JSON, String

from guard.core.config import settings
from guard.models.base import (
    GUID,
    TABLE_PREFIX,
    Base,
    CreatedUpdatedAtMixin,
    ExpiresAtMixin,
)
from guard.models.client import Client


class ACR(StrEnum):
    LEVEL_0 = "0"  # 匿名/最低保证
    LEVEL_1 = "1"  # 单因素认证
    LEVEL_2 = "2"
    LEVEL_3 = "3"


class LoginSession(Base, CreatedUpdatedAtMixin, ExpiresAtMixin):
    __tablename__ = "login_sessions"
    __lifetime_seconds = settings.LOGIN_SESSION_LIFETIME_SECONDS

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column(
        String(length=255),
        default=secrets.token_urlsafe,
        nullable=False,
        index=True,
        unique=True,
    )
    response_type: Mapped[str] = mapped_column(String(length=255), nullable=False)
    response_mode: Mapped[str] = mapped_column(String(length=255), nullable=False)
    redirect_uri: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    prompt: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    state: Mapped[str | None] = mapped_column(String(length=2048), nullable=True)
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

    client_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(Client.id, ondelete="CASCADE"), nullable=False
    )
    client: Mapped[Client] = relationship()

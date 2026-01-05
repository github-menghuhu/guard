from enum import StrEnum
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import JSON, String

from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    Prompt,
    ResponseMode,
    ResponseTypes,
    Scopes,
    UUIDPrimaryKeyMixin,
)
from guard.models.client import Client
from guard.models.user import User


class ACR(StrEnum):
    LEVEL_0 = "0"  # 匿名/最低保证
    LEVEL_1 = "1"  # 单因素认证
    LEVEL_2 = "2"
    LEVEL_3 = "3"


class AuthorizationRequests(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "authorization_requests"

    response_type: Mapped[ResponseTypes] = mapped_column(
        Enum(ResponseTypes), nullable=False
    )
    response_mode: Mapped[ResponseMode] = mapped_column(
        Enum(ResponseTypes), nullable=False
    )
    redirect_uri: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[list[Scopes]] = mapped_column(JSON, nullable=False, default=list)
    prompt: Mapped[Prompt] = mapped_column(Enum(Prompt), nullable=False)
    state: Mapped[str | None] = mapped_column(String(length=2048), nullable=True)
    nonce: Mapped[str | None] = mapped_column(String(length=2048), nullable=True)
    code_challenge: Mapped[str | None] = mapped_column(
        String(length=255), nullable=True
    )
    code_challenge_method: Mapped[str | None] = mapped_column(
        String(length=255), nullable=True
    )

    user_id: Mapped[UUID | None] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=True
    )
    user: Mapped[User | None] = relationship()
    client_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey(Client.id, ondelete="CASCADE"), nullable=False
    )
    client: Mapped[Client] = relationship()

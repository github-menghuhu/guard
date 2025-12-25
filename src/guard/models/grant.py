import uuid

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import UniqueConstraint

from guard.models.base import (
    GUID,
    Base,
    CreatedUpdatedAtMixin,
    UUIDPrimaryKeyMixin,
)
from guard.models.client import Client
from guard.models.user import User


class Grant(UUIDPrimaryKeyMixin, Base, CreatedUpdatedAtMixin):
    __tablename__ = "grants"
    __table_args__ = (UniqueConstraint("user_id", "client_id"),)

    scope: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship()

    client_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey(Client.id, ondelete="CASCADE"), nullable=False
    )
    client: Mapped[Client] = relationship()

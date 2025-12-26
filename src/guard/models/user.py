from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from guard.models.base import (
    Base,
    CreatedUpdatedAtMixin,
    UUIDPrimaryKeyMixin,
)
from guard.utils.random import generate_random_string


class User(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(length=255), default=generate_random_string, nullable=False
    )
    phone: Mapped[str | None] = mapped_column(
        String(length=20), index=True, nullable=True
    )
    phone_verified: Mapped[bool] = mapped_column(
        Boolean, index=True, default=False, nullable=False
    )
    email: Mapped[str] = mapped_column(String(length=320), index=True, nullable=False)
    email_verified: Mapped[bool] = mapped_column(
        Boolean, index=True, default=False, nullable=False
    )
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

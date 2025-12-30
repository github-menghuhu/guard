from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from guard.models.base import (
    Base,
    CreatedUpdatedAtMixin,
    UUIDPrimaryKeyMixin,
)


class Permission(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    code: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guard.models.base import (
    Base,
    CreatedUpdatedAtMixin,
    UUIDPrimaryKeyMixin,
    get_prefixed_tablename,
)
from guard.models.permission import Permission


class Role(UUIDPrimaryKeyMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    permissions: Mapped[list[Permission]] = relationship(
        secondary=get_prefixed_tablename("roles_permissions"), lazy="selectin"
    )

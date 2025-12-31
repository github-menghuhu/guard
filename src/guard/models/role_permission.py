from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from guard.models.base import GUID, Base
from guard.models.permission import Permission
from guard.models.role import Role


class RolePermission(Base):
    __tablename__ = "roles_permissions"

    role_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey(Role.id, ondelete="CASCADE"), nullable=False, primary_key=True
    )
    permission_id: Mapped[UUID] = mapped_column(
        GUID,
        ForeignKey(Permission.id, ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

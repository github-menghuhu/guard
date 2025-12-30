from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from guard.models.base import GUID, Base
from guard.models.permission import Permission
from guard.models.user import User


class UserPermission(Base):
    __tablename__ = "users_permissions"

    user_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False, primary_key=True
    )
    permission_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey(Permission.id, ondelete="CASCADE"), nullable=False, primary_key=True
    )

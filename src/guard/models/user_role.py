from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from guard.models.base import GUID, Base
from guard.models.role import Role
from guard.models.user import User


class UserRole(Base):
    __tablename__ = "users_roles"

    user_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False, primary_key=True
    )
    role_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey(Role.id, ondelete="CASCADE"), nullable=False, primary_key=True
    )

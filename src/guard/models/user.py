import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from guard.models import Base, GUID, TimestampMixin, SoftDeleteMixin, Tenant
from guard.utils.random import generate_random_string


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=255), default=generate_random_string, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(length=20), index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(length=320), index=True, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, index=True, default=False, nullable=False)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(GUID, index=True, nullable=False)

    tenant: Mapped[Tenant] = relationship("Tenant", primaryjoin="User.tenant_id == Tenant.id")

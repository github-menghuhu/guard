import uuid
from enum import StrEnum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from guard.models import GUID, Base, SoftDeleteMixin, TimestampMixin


class TenantStatus(StrEnum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"


class Tenant(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    slug: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus), nullable=False, default=TenantStatus.ENABLE
    )
    contact_person: Mapped[str | None] = mapped_column(String(length=50), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(length=20), nullable=True)

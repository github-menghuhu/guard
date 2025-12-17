import uuid
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guard.models.base import (
    GUID,
    TABLE_PREFIX,
    Base,
    CreatedUpdatedAtMixin,
)

if TYPE_CHECKING:
    from guard.models.client import Client


class TenantStatus(StrEnum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"


class Tenant(Base, CreatedUpdatedAtMixin):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    slug: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus, name=f"{TABLE_PREFIX}tenant_status"),
        nullable=False,
        default=TenantStatus.ENABLE,
    )
    contact_person: Mapped[str | None] = mapped_column(String(length=50), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(length=20), nullable=True)

    clients: Mapped[list["Client"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan", passive_deletes=True
    )

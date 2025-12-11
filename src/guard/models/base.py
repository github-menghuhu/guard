import uuid

from datetime import datetime, timezone
from sqlalchemy import MetaData, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import CHAR, TypeDecorator
from sqlalchemy.dialects import mysql, postgresql
from guard.utils import datetime as utils_datetime


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utils_datetime.get_datetime_now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utils_datetime.get_datetime_now(timezone.utc), nullable=False,
        onupdate=utils_datetime.get_datetime_now(timezone.utc)
    )


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)


class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(postgresql.UUID())
        elif dialect.name == "mysql":
            return dialect.type_descriptor(mysql.BINARY(16))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        if dialect.name == "postgresql":
            return value
        elif dialect.name == "mysql":
            return value.bytes
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        if dialect.name == "mysql":
            if isinstance(value, bytes):
                return uuid.UUID(bytes=value)
            return uuid.UUID(value) if not isinstance(value, uuid.UUID) else value

        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "%(table_name)s_%(column_0_N_name)s_key",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    pass

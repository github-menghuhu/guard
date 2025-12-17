import base64
import functools
import uuid
from datetime import UTC, datetime

from cryptography.fernet import Fernet
from sqlalchemy import Boolean, ColumnElement, DateTime, MetaData, Text
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, mapped_column
from sqlalchemy.types import CHAR, TypeDecorator

from guard.core.config import settings
from guard.utils import datetime as utils_datetime


class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        if value.tzinfo is None:
            raise ValueError(  # noqa: TRY003
                f"接收到: {value} 请提供带时区的时间，或使用 .replace(tzinfo=timezone.utc) 明确时区。"
            )

        if dialect.name == "mysql":
            return value.astimezone(UTC).replace(tzinfo=None)

        return value.astimezone(UTC)

    def process_result_value(self, value, dialect):
        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)

        return value


class CreatedUpdatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(timezone=True),
        default=utils_datetime.get_now,
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(timezone=True),
        default=utils_datetime.get_now,
        nullable=False,
        index=True,
        onupdate=utils_datetime.get_now,
    )


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        UTCDateTime(timezone=True), default=None, nullable=True
    )


class ExpiresAtMixin:
    @declared_attr
    def expires_at(cls) -> MappedColumn[datetime]:
        try:
            default_lifetime_seconds = getattr(
                cls,
                "__lifetime_seconds",
            )
            default = functools.partial(
                utils_datetime.get_default_expires_at,
                timedelta_seconds=default_lifetime_seconds,
            )
        except AttributeError:
            default = None
        return mapped_column(
            UTCDateTime(timezone=True), nullable=False, index=True, default=default
        )

    @hybrid_property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(UTC)

    @is_expired.inplace.expression
    @classmethod
    def _is_expired_expression(cls) -> ColumnElement[bool]:
        return cls.expires_at < datetime.now(UTC)


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


class EncryptedString(TypeDecorator):
    impl = Text
    cache_ok = True

    _cipher_suite = Fernet(settings.ENCRYPTION_KEY)

    def process_bind_param(self, value, dialect):
        if value is not None:
            encrypted_value = self._cipher_suite.encrypt(value.encode("utf-8"))
            return base64.urlsafe_b64encode(encrypted_value).decode("utf-8")
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            decrypted_value = self._cipher_suite.decrypt(
                base64.urlsafe_b64decode(value)
            )
            return decrypted_value.decode("utf-8")
        return value


TABLE_PREFIX = settings.DATABASE_TABLE_PREFIX


def get_prefixed_tablename(name: str) -> str:
    return f"{TABLE_PREFIX}{name}"


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

    def __init_subclass__(cls) -> None:
        cls.__tablename__ = get_prefixed_tablename(cls.__tablename__)
        super().__init_subclass__()

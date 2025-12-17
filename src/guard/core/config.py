import os
from enum import StrEnum
from functools import lru_cache

from pydantic import ValidationError, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseType(StrEnum):
    POSTGRESQL = "POSTGRESQL"
    MYSQL = "MYSQL"


class Settings(BaseSettings):
    # 项目根目录
    @computed_field  # type: ignore[prop-decorator]
    @property
    def BASE_DIR(self) -> str:
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )

    # 全局时区
    TIME_ZONE: str = "Asia/Shanghai"

    # 关系数据库
    DATABASE_TYPE: DatabaseType
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_TABLE_PREFIX: str = "guard_"
    IS_PRINT_SQL: bool = False

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASSWORD: str

    # 日志等级
    LOG_LEVEL: LogLevel = LogLevel.INFO

    # 全局密钥
    SECRET: str

    # 跨域允许列表
    ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:9000",
    ]

    # 加密密钥
    ENCRYPTION_KEY: bytes

    # 默认授权码、访问令牌和ID令牌、刷新令牌过期时间
    DEFAULT_AUTHORIZATION_CODE_LIFETIME_SECONDS: int = 600
    DEFAULT_ACCESS_ID_TOKEN_LIFETIME_SECONDS: int = 3600 * 24
    DEFAULT_REFRESH_TOKEN_LIFETIME_SECONDS: int = 3600 * 24 * 7

    # 注册会话过期时间
    REGISTRATION_SESSION_LIFETIME_SECONDS: int = 3600
    # 登录会话过期时间
    LOGIN_SESSION_LIFETIME_SECONDS: int = 3600
    # OAuth会话过期时间
    OAUTH_SESSION_LIFETIME_SECONDS: int = 3600

    # 用户会话过期时间
    SESSION_LIFETIME_SECONDS: int = 3600 * 24 * 7

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        # env_nested_delimiter='__', # 嵌套结构时用这个参数分割
        case_sensitive=True,
    )


@lru_cache
def _get_settings() -> Settings:
    try:
        settings = Settings(_env_file=".env.dev")  # type: ignore[call-arg]
    except ValidationError as e:
        raise RuntimeError(  # noqa: TRY003
            f"""
            环境变量加载异常，请检查.env文件！\n
            异常信息：{e.errors()}
            """
        )

    return settings


settings = _get_settings()

__all__ = ["settings"]

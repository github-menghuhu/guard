import os

from enum import StrEnum
from functools import lru_cache
from pydantic import computed_field
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
    @computed_field
    @property
    def BASE_DIR(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    # 全局时区
    TIME_ZONE: str = "Asia/Shanghai"

    # 关系数据库
    DATABASE_TYPE: DatabaseType
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    IS_PRINT_SQL: bool = False

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASSWORD: str

    # 日志等级
    LOG_LEVEL: LogLevel = LogLevel.INFO

    # 全局密钥
    SECRET: str

    model_config = SettingsConfigDict(
        env_file='.env.dev',
        env_file_encoding='utf-8',
        # env_nested_delimiter='__', # 嵌套结构时用这个参数分割
        case_sensitive=True,
    )


@lru_cache
def _get_settings() -> Settings:
    try:
        settings = Settings()
    except Exception as e:
        raise Exception(
            f"""
            环境变量加载异常，请检查.env文件！\n
            异常信息：{e}
            """
        )

    return settings


settings = _get_settings()

__all__ = ["settings"]

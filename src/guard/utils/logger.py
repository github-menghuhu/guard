import json
import logging
import sys
from types import FrameType
from typing import TYPE_CHECKING

from loguru import logger

from guard.core.config import settings

if TYPE_CHECKING:
    from loguru import Record

LOG_LEVEL = settings.LOG_LEVEL


class InterceptHandler(logging.Handler):
    def emit(self, record) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame: FrameType | None = sys._getframe(6)
        depth = 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def stdout_format(record: "Record") -> str:
    record["extra"]["extra_json"] = json.dumps(record["extra"])
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> - "
        "{extra[extra_json]}"
        "\n{exception}"
    )


def init_logger(level="INFO", intercept_fastapi=True) -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        format=stdout_format,
        level=level,
        backtrace=True,
        diagnose=False,
    )

    if intercept_fastapi:
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        for logger_name in [
            "uvicorn",
            "uvicorn.error",
            "uvicorn.access",
            "fastapi",
            "api_exception",
            "sqlalchemy.engine.Engine",
        ]:
            logging.getLogger(logger_name).handlers = [InterceptHandler()]
            logging.getLogger(logger_name).propagate = False


__all__ = ["init_logger", "logger"]

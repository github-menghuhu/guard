from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from fastapi import FastAPI
from guard.core.config import settings
from guard.utils.log import init_logger, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    init_logger(settings.LOG_LEVEL.value)

    logger.info("Guard Server started")

    yield

    logger.info("Guard Server stopped")


app = FastAPI(lifespan=lifespan)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    # 检查数据库
    pass
    # 检查其他服务
    return {"message": "Everything is ready."}

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from guard import __version__
from guard.core.config import settings
from guard.middlewares import RequestIDMiddleware, origins
from guard.utils.logger import init_logger, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    init_logger(settings.LOG_LEVEL.value)

    logger.info("Guard Server started")

    yield

    logger.info("Guard Server stopped")


app = FastAPI(title="Fief Authentication API", lifespan=lifespan, version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    # 检查数据库
    pass
    # 检查其他服务
    return {"message": "Everything is ready."}

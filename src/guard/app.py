from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from api_exception import APIResponse, register_exception_handlers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from guard import __version__
from guard.apps.admin import admin_router
from guard.apps.auth import auth_router
from guard.core.config import settings
from guard.middlewares import (
    RequestIDMiddleware,
    allow_headers,
    allow_methods,
    allow_origins,
)
from guard.utils.logger import init_logger, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    init_logger(settings.LOG_LEVEL.value)

    logger.info("Guard Server started")

    yield

    logger.info("Guard Server stopped")


app = FastAPI(
    title="Guard Authentication API",
    lifespan=lifespan,
    version=__version__,
    responses=APIResponse.default(),  # type: ignore[arg-type]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)
app.add_middleware(RequestIDMiddleware)

app.include_router(auth_router)
app.include_router(admin_router)

register_exception_handlers(
    app=app,
    log_traceback=False,
    log_traceback_unhandled_exception=True,
    use_fallback_middleware=True,
)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    # 检查数据库
    pass
    # 检查其他服务
    return {"message": "Everything is ready."}

from fastapi import APIRouter

from .auth import router

auth_router = APIRouter(tags=["auth"])
auth_router.include_router(router)

__all__ = ["auth_router"]

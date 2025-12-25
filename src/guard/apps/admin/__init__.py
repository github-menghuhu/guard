from fastapi import APIRouter

from .client import router as client_router

admin_router = APIRouter(prefix="/admin", tags=["admin"])
admin_router.include_router(client_router)

__all__ = ["admin_router"]

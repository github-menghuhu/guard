from fastapi import APIRouter

from .client import router as client_router
from .permission import router as permission_router
from .role import router as role_router
from .user import router as user_router

admin_router = APIRouter(prefix="/admin", tags=["admin"])
admin_router.include_router(client_router)
admin_router.include_router(user_router)
admin_router.include_router(role_router)
admin_router.include_router(permission_router)

__all__ = ["admin_router"]

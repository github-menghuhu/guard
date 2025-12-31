from .base import BaseRepository, Paginate
from .client import ClientRepository
from .permission import PermissionRepository
from .role import RoleRepository
from .user import UserRepository
from .oauth_provider import OAuthProviderRepository

__all__ = [
    "BaseRepository",
    "Paginate",
    "ClientRepository",
    "UserRepository",
    "RoleRepository",
    "PermissionRepository",
    "OAuthProviderRepository",
]

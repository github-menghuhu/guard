from guard.core.config import settings

allow_origins = settings.ORIGINS
allow_methods = settings.METHODS
allow_headers = settings.HEADERS

__all__ = ["allow_origins", "allow_methods", "allow_headers"]

from guard.models import AuthorizationCode
from guard.repositories import BaseRepository


class AuthorizationCodeRepository(BaseRepository[AuthorizationCode]):
    _model = AuthorizationCode

    pass

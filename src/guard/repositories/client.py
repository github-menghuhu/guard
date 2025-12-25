from guard.models import Client
from guard.repositories import BaseRepository


class ClientRepository(BaseRepository[Client]):
    _model = Client

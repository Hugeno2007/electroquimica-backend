from app.models import SENSORES
from app.repositories.base import BaseRepository


class SensorRepositorio(BaseRepository):
    """Repositorio de sensores."""

    def __init__(self):
        super().__init__(SENSORES)

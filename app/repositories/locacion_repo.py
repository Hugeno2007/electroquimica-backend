from app.models import LOCACIONES
from app.repositories.base import BaseRepository


class LocacionRepositorio(BaseRepository):
    """Repositorio de locaciones."""

    def __init__(self):
        super().__init__(LOCACIONES)

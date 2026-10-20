from app.models import LECTURAS
from app.repositories.base import BaseRepository


class LecturaRepositorio(BaseRepository):
    """Repositorio de lecturas de sensores."""

    def __init__(self):
        super().__init__(LECTURAS)

from app.models import DPTOS
from app.repositories.base import BaseRepository


class DptoRepositorio(BaseRepository):
    """Repositorio de departamentos."""

    def __init__(self):
        super().__init__(DPTOS)

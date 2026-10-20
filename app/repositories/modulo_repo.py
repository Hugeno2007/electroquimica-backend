from app.models import MODULOS
from app.repositories.base import BaseRepository


class ModuloRepositorio(BaseRepository):
    """Repositorio de módulos."""

    def __init__(self):
        super().__init__(MODULOS)

from app.models import USUARIOS
from app.repositories.base import BaseRepository


class UsuarioRepositorio(BaseRepository):
    """Repositorio de usuarios."""

    def __init__(self):
        super().__init__(USUARIOS)

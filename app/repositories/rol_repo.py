from app.models import ROLES
from app.repositories.base import BaseRepository


class RolRepositorio(BaseRepository):
    """Repositorio de roles."""

    def __init__(self):
        super().__init__(ROLES)

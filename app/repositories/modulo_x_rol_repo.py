from app.models import MODULO_X_ROL
from app.repositories.base import BaseRepository


class ModuloXRolRepositorio(BaseRepository):
    """Repositorio de permisos asociados a roles y módulos."""

    def __init__(self):
        super().__init__(MODULO_X_ROL)

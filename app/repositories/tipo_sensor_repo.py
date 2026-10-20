from app.models import TIPOS_SENSOR
from app.repositories.base import BaseRepository


class TipoSensorRepositorio(BaseRepository):
    """Repositorio de tipos de sensor."""

    def __init__(self):
        super().__init__(TIPOS_SENSOR)

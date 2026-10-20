from app.models import ASIGNACIONES_SENSOR
from app.repositories.base import BaseRepository


class AsignacionSensorRepositorio(BaseRepository):
    """Repositorio de asignaciones de sensores."""

    def __init__(self):
        super().__init__(ASIGNACIONES_SENSOR)

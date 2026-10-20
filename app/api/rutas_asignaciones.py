from app.api.crud import crear_router_crud
from app.api.schemas import (
    AsignacionSensorCreate,
    AsignacionSensorRead,
    AsignacionSensorUpdate,
)
from app.models import ASIGNACIONES_SENSOR
from app.repositories.asignacion_sensor_repo import AsignacionSensorRepositorio

repositorio_asignaciones = AsignacionSensorRepositorio()

router = crear_router_crud(
    "/asignaciones-sensor",
    "Asignaciones",
    ASIGNACIONES_SENSOR,
    AsignacionSensorCreate,
    AsignacionSensorUpdate,
    AsignacionSensorRead,
    repository=repositorio_asignaciones,
)

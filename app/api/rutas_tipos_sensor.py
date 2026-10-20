from app.api.crud import crear_router_crud
from app.api.schemas import TipoSensorCreate, TipoSensorRead, TipoSensorUpdate
from app.models import TIPOS_SENSOR
from app.repositories.tipo_sensor_repo import TipoSensorRepositorio

repositorio_tipos_sensor = TipoSensorRepositorio()

router = crear_router_crud(
    "/tipos-sensor",
    "Tipos de sensor",
    TIPOS_SENSOR,
    TipoSensorCreate,
    TipoSensorUpdate,
    TipoSensorRead,
    repository=repositorio_tipos_sensor,
)

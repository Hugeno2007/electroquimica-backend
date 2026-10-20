from app.api.crud import crear_router_crud
from app.api.schemas import SensorCreate, SensorRead, SensorUpdate
from app.models import SENSORES
from app.repositories.sensor_repo import SensorRepositorio

repositorio_sensores = SensorRepositorio()

router = crear_router_crud(
    "/sensores",
    "Sensores",
    SENSORES,
    SensorCreate,
    SensorUpdate,
    SensorRead,
    repository=repositorio_sensores,
)

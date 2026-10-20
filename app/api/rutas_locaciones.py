from app.api.crud import crear_router_crud
from app.api.schemas import LocacionCreate, LocacionRead, LocacionUpdate
from app.models import LOCACIONES
from app.repositories.locacion_repo import LocacionRepositorio

repositorio_locaciones = LocacionRepositorio()

router = crear_router_crud(
    "/locaciones",
    "Locaciones",
    LOCACIONES,
    LocacionCreate,
    LocacionUpdate,
    LocacionRead,
    repository=repositorio_locaciones,
)

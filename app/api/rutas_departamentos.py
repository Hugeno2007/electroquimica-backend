from app.api.crud import crear_router_crud
from app.api.schemas import DptoCreate, DptoRead, DptoUpdate
from app.models import DPTOS
from app.repositories.dpto_repo import DptoRepositorio

repositorio_departamentos = DptoRepositorio()

router = crear_router_crud(
    "/dptos",
    "Departamentos",
    DPTOS,
    DptoCreate,
    DptoUpdate,
    DptoRead,
    repository=repositorio_departamentos,
)

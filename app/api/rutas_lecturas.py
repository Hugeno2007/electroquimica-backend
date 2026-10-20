from app.api.crud import crear_router_crud
from app.api.schemas import LecturaCreate, LecturaRead, LecturaUpdate
from app.models import LECTURAS
from app.repositories.lectura_repo import LecturaRepositorio

repositorio_lecturas = LecturaRepositorio()

router = crear_router_crud(
    "/lecturas",
    "Lecturas",
    LECTURAS,
    LecturaCreate,
    LecturaUpdate,
    LecturaRead,
    repository=repositorio_lecturas,
)

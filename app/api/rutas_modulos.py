from app.api.crud import crear_router_crud
from app.api.schemas import ModuloCreate, ModuloRead, ModuloUpdate
from app.models import MODULOS
from app.repositories.modulo_repo import ModuloRepositorio

repositorio_modulos = ModuloRepositorio()

router = crear_router_crud(
    "/modulos",
    "Módulos",
    MODULOS,
    ModuloCreate,
    ModuloUpdate,
    ModuloRead,
    repository=repositorio_modulos,
)

from app.api.crud import crear_router_crud
from app.api.schemas import ModuloXRolCreate, ModuloXRolRead, ModuloXRolUpdate
from app.models import MODULO_X_ROL
from app.repositories.modulo_x_rol_repo import ModuloXRolRepositorio

repositorio_permisos = ModuloXRolRepositorio()

router = crear_router_crud(
    "/modulo-x-rol",
    "Permisos por rol",
    MODULO_X_ROL,
    ModuloXRolCreate,
    ModuloXRolUpdate,
    ModuloXRolRead,
    repository=repositorio_permisos,
)

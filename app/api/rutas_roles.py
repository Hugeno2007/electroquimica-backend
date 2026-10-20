from app.api.crud import crear_router_crud
from app.api.schemas import RolCreate, RolRead, RolUpdate
from app.models import ROLES
from app.repositories.rol_repo import RolRepositorio

repositorio_roles = RolRepositorio()

router = crear_router_crud(
    "/roles",
    "Roles",
    ROLES,
    RolCreate,
    RolUpdate,
    RolRead,
    repository=repositorio_roles,
)

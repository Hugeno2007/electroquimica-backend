from app.api.crud import crear_router_crud
from app.api.schemas import UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.models import USUARIOS
from app.repositories.usuario_repo import UsuarioRepositorio

repositorio_usuarios = UsuarioRepositorio()

router = crear_router_crud(
    "/usuarios",
    "Usuarios",
    USUARIOS,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioRead,
    repository=repositorio_usuarios,
)

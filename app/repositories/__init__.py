from app.repositories.base import BaseRepository, Repository
from app.repositories.asignacion_sensor_repo import AsignacionSensorRepositorio
from app.repositories.dpto_repo import DptoRepositorio
from app.repositories.lectura_repo import LecturaRepositorio
from app.repositories.locacion_repo import LocacionRepositorio
from app.repositories.modulo_repo import ModuloRepositorio
from app.repositories.modulo_x_rol_repo import ModuloXRolRepositorio
from app.repositories.rol_repo import RolRepositorio
from app.repositories.sensor_repo import SensorRepositorio
from app.repositories.tipo_sensor_repo import TipoSensorRepositorio
from app.repositories.usuario_repo import UsuarioRepositorio

__all__ = [
    "BaseRepository",
    "Repository",
    "AsignacionSensorRepositorio",
    "DptoRepositorio",
    "LecturaRepositorio",
    "LocacionRepositorio",
    "ModuloRepositorio",
    "ModuloXRolRepositorio",
    "RolRepositorio",
    "SensorRepositorio",
    "TipoSensorRepositorio",
    "UsuarioRepositorio",
]


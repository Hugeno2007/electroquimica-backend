from app.models.base import EntityModel
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.modulo import Modulo
from app.models.modulo_x_rol import ModuloXRol
from app.models.tipo_sensor import TipoSensor
from app.models.sensor import Sensor
from app.models.dpto import Dpto
from app.models.locacion import Locacion
from app.models.asignacion_sensor import AsignacionSensor
from app.models.lectura import Lectura
from app.models.entities import (
    ASIGNACIONES_SENSOR,
    DPTOS,
    ENTITY_MODELS,
    LECTURAS,
    LOCACIONES,
    MODULOS,
    MODULO_X_ROL,
    ROLES,
    SENSORES,
    TIPOS_SENSOR,
    USUARIOS,
    Entity,
)

ENTITY_MODEL_TYPES = tuple(ENTITY_MODELS.values())

__all__ = [
    "EntityModel",
    "Usuario",
    "Rol",
    "Modulo",
    "ModuloXRol",
    "TipoSensor",
    "Sensor",
    "Dpto",
    "Locacion",
    "AsignacionSensor",
    "Lectura",
    "ENTITY_MODEL_TYPES",
    "Entity",
    "ENTITY_MODELS",
    "USUARIOS",
    "ROLES",
    "MODULOS",
    "MODULO_X_ROL",
    "TIPOS_SENSOR",
    "SENSORES",
    "DPTOS",
    "LOCACIONES",
    "ASIGNACIONES_SENSOR",
    "LECTURAS",
]

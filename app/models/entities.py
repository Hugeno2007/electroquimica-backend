from app.models.base import EntityModel as Entity
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

USUARIOS = Usuario
ROLES = Rol
MODULOS = Modulo
MODULO_X_ROL = ModuloXRol
TIPOS_SENSOR = TipoSensor
SENSORES = Sensor
DPTOS = Dpto
LOCACIONES = Locacion
ASIGNACIONES_SENSOR = AsignacionSensor
LECTURAS = Lectura

ENTITY_MODELS = {
    "usuarios": USUARIOS,
    "roles": ROLES,
    "modulos": MODULOS,
    "modulo_x_rol": MODULO_X_ROL,
    "tipos_sensor": TIPOS_SENSOR,
    "sensores": SENSORES,
    "dptos": DPTOS,
    "locaciones": LOCACIONES,
    "asignaciones_sensor": ASIGNACIONES_SENSOR,
    "lecturas": LECTURAS,
}

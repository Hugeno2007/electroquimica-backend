from fastapi import APIRouter

from app.api import (
    rutas_asignaciones as asignaciones,
    rutas_departamentos as departamentos,
    rutas_lecturas as lecturas,
    rutas_locaciones as locaciones,
    rutas_modulos as modulos,
    rutas_permisos as permisos,
    rutas_roles as roles,
    rutas_sensores as sensores,
    rutas_tipos_sensor as tipos_sensor,
    rutas_usuarios as usuarios,
)


api_router = APIRouter()


@api_router.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok"}


for modulo_rutas in (
    usuarios,
    roles,
    modulos,
    permisos,
    tipos_sensor,
    sensores,
    departamentos,
    locaciones,
    asignaciones,
    lecturas,
):
    api_router.include_router(modulo_rutas.router)

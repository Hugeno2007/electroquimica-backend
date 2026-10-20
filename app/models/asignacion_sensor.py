from datetime import datetime
from typing import ClassVar, Literal

from pydantic import Field

from app.models.base import EntityModel


class AsignacionSensor(EntityModel):
    table: ClassVar[str] = "asignacion_sensor"
    create_required: ClassVar[tuple[str, ...]] = ("idusuario", "idsensor")
    create_defaults: ClassVar[dict[str, object]] = {"estado": "ACTIVA"}

    id: int | None = None
    idusuario: int | None = Field(default=None, gt=0)
    idsensor: int | None = Field(default=None, gt=0)
    fecha_asignacion: datetime | None = None
    fecha_fin: datetime | None = None
    estado: Literal["ACTIVA", "FINALIZADA"] | None = None

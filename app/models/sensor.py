from datetime import datetime
from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class Sensor(EntityModel):
    table: ClassVar[str] = "sensor"
    create_required: ClassVar[tuple[str, ...]] = ("idtiposensor", "codigo", "nombre")
    create_defaults: ClassVar[dict[str, object]] = {"estado": True}

    id: int | None = None
    idtiposensor: int | None = Field(default=None, gt=0)
    codigo: str | None = Field(default=None, min_length=1, max_length=50)
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    modelo: str | None = Field(default=None, max_length=100)
    fabricante: str | None = Field(default=None, max_length=100)
    ubicacion_fisica: str | None = Field(default=None, max_length=255)
    estado: bool | None = None
    fecha_instalacion: datetime | None = None

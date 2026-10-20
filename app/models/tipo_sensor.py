from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class TipoSensor(EntityModel):
    table: ClassVar[str] = "tipo_sensor"
    create_required: ClassVar[tuple[str, ...]] = ("nombre", "unidad_medida")
    create_defaults: ClassVar[dict[str, object]] = {"estado": True}

    id: int | None = None
    nombre: str | None = Field(default=None, min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, max_length=255)
    unidad_medida: str | None = Field(default=None, min_length=1, max_length=20)
    fabricante: str | None = Field(default=None, max_length=100)
    modelo: str | None = Field(default=None, max_length=100)
    estado: bool | None = None

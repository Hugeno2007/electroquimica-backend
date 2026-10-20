from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class Locacion(EntityModel):
    table: ClassVar[str] = "locacion"
    create_required: ClassVar[tuple[str, ...]] = ("iddpto", "nombre")
    create_defaults: ClassVar[dict[str, object]] = {"estado": True}

    id: int | None = None
    iddpto: int | None = Field(default=None, gt=0)
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    direccion: str | None = Field(default=None, max_length=255)
    latitud: float | None = Field(default=None, ge=-90, le=90)
    longitud: float | None = Field(default=None, ge=-180, le=180)
    estado: bool | None = None

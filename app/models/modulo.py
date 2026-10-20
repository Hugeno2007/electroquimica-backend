from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class Modulo(EntityModel):
    table: ClassVar[str] = "modulo"
    create_required: ClassVar[tuple[str, ...]] = ("nombre",)
    create_defaults: ClassVar[dict[str, object]] = {"estado": True}

    id: int | None = None
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    ruta: str | None = Field(default=None, max_length=255)
    icono: str | None = Field(default=None, max_length=100)
    estado: bool | None = None

from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class Rol(EntityModel):
    table: ClassVar[str] = "rol"
    create_required: ClassVar[tuple[str, ...]] = ("nombre",)
    create_defaults: ClassVar[dict[str, object]] = {"estado": True}

    id: int | None = None
    nombre: str | None = Field(default=None, min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool | None = None

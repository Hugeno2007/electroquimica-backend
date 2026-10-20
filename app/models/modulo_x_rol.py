from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class ModuloXRol(EntityModel):
    table: ClassVar[str] = "modulo_x_rol"
    create_required: ClassVar[tuple[str, ...]] = ("idrol", "idmodulo")
    create_defaults: ClassVar[dict[str, object]] = {"estado": True}

    id: int | None = None
    idrol: int | None = Field(default=None, gt=0)
    idmodulo: int | None = Field(default=None, gt=0)
    estado: bool | None = None

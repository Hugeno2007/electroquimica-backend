from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class Usuario(EntityModel):
    table: ClassVar[str] = "usuarios"
    create_required: ClassVar[tuple[str, ...]] = (
        "nombre",
        "apellido",
        "correo",
        "password",
        "idrol",
    )
    create_defaults: ClassVar[dict[str, object]] = {"estado": True}

    id: int | None = None
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    apellido: str | None = Field(default=None, min_length=1, max_length=100)
    correo: str | None = Field(default=None, min_length=3, max_length=150)
    password: str | None = Field(
        default=None,
        min_length=10,
        max_length=255,
        exclude=True,
        description="Se recibe para crear o cambiar la contraseña y se guarda cifrada.",
    )
    idrol: int | None = Field(default=None, gt=0)
    estado: bool | None = None

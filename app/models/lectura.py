from datetime import datetime
from typing import ClassVar

from pydantic import Field

from app.models.base import EntityModel


class Lectura(EntityModel):
    table: ClassVar[str] = "lectura"
    create_required: ClassVar[tuple[str, ...]] = ("idsensor", "idlocacion", "valor")
    order_by: ClassVar[str] = "fecha_hora DESC, id DESC"

    id: int | None = None
    idsensor: int | None = Field(default=None, gt=0)
    idlocacion: int | None = Field(default=None, gt=0)
    valor: float | None = Field(default=None, ge=0, le=14)
    temperatura: float | None = Field(default=None, ge=-999.99, le=999.99)
    fecha_hora: datetime | None = None
    calidad: str | None = Field(default=None, max_length=50)

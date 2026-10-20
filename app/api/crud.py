import sqlite3

import psycopg2
from fastapi import APIRouter, HTTPException, Query

from app.core.database import database_connection
from app.models import EntityModel
from app.repositories import BaseRepository


_INTEGRITY_ERRORS = (sqlite3.IntegrityError, psycopg2.IntegrityError)


def _conflict() -> None:
    raise HTTPException(
        status_code=409,
        detail=(
            "No se pudo guardar el registro. Verifica que los códigos y correos no estén "
            "repetidos y que las relaciones existan."
        ),
    )


def _not_found() -> None:
    raise HTTPException(status_code=404, detail="Registro no encontrado.")


def crear_router_crud(
    path: str,
    tag: str,
    entity: type[EntityModel],
    create_schema,
    update_schema,
    read_schema,
    repository: BaseRepository | None = None,
) -> APIRouter:
    """Crea las rutas REST comunes para un recurso basado en EntityModel."""
    router = APIRouter()
    repository = repository or BaseRepository(entity)
    if repository.entity is not entity:
        raise ValueError("El repositorio debe corresponder al modelo de la ruta.")
    slug = path.strip("/").replace("-", "_")

    def listar(
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=100, ge=1, le=100),
    ):
        with database_connection() as connection:
            return repository.list(connection, page, page_size)

    router.add_api_route(
        f"{path}/",
        listar,
        methods=["GET"],
        response_model=list[read_schema],
        tags=[tag],
        name=f"{slug}_list",
        summary=f"Listar {tag.lower()}",
    )

    def obtener(item_id):
        with database_connection() as connection:
            item = repository.get(connection, item_id)
        if item is None:
            _not_found()
        return item

    obtener.__annotations__ = {"item_id": int}
    router.add_api_route(
        f"{path}/{{item_id}}",
        obtener,
        methods=["GET"],
        response_model=read_schema,
        tags=[tag],
        name=f"{slug}_get",
        summary=f"Consultar {tag.lower()} por ID",
    )

    def crear(payload):
        try:
            with database_connection() as connection:
                return repository.create(connection, payload)
        except _INTEGRITY_ERRORS:
            _conflict()

    crear.__annotations__ = {"payload": create_schema}
    router.add_api_route(
        f"{path}/",
        crear,
        methods=["POST"],
        response_model=read_schema,
        status_code=201,
        tags=[tag],
        name=f"{slug}_create",
        summary=f"Crear {tag.lower()}",
    )

    def actualizar(item_id, payload):
        try:
            with database_connection() as connection:
                item = repository.update(connection, item_id, payload)
        except _INTEGRITY_ERRORS:
            _conflict()
        if item is None:
            _not_found()
        return item

    actualizar.__annotations__ = {"item_id": int, "payload": update_schema}
    router.add_api_route(
        f"{path}/{{item_id}}",
        actualizar,
        methods=["PUT"],
        response_model=read_schema,
        tags=[tag],
        name=f"{slug}_update",
        summary=f"Actualizar {tag.lower()}",
    )

    def eliminar(item_id):
        try:
            with database_connection() as connection:
                deleted = repository.delete(connection, item_id)
        except _INTEGRITY_ERRORS:
            _conflict()
        if not deleted:
            _not_found()
        return None

    eliminar.__annotations__ = {"item_id": int}
    router.add_api_route(
        f"{path}/{{item_id}}",
        eliminar,
        methods=["DELETE"],
        status_code=204,
        response_model=None,
        tags=[tag],
        name=f"{slug}_delete",
        summary=f"Eliminar {tag.lower()}",
    )

    return router


__all__ = ["crear_router_crud"]

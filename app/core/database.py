from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator

import psycopg2
from psycopg2.extras import RealDictCursor

from app.core.config import BASE_DIR, settings
from app.models.schema import create_schema


def is_postgres() -> bool:
    return settings.database_url.startswith(("postgres://", "postgresql://", "postgresql+psycopg2://"))


def placeholder() -> str:
    return "%s" if is_postgres() else "?"


def _sqlite_path() -> str:
    prefix = "sqlite:///"
    if not settings.database_url.startswith(prefix):
        raise ValueError("DATABASE_URL debe comenzar con sqlite:/// o usar PostgreSQL.")
    raw_path = settings.database_url[len(prefix):]
    path = Path(raw_path)
    if not path.is_absolute():
        path = BASE_DIR / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


class Database:
    """Entrega conexiones usando la configuración cargada desde el entorno."""

    def get_connection(self):
        if is_postgres():
            url = settings.database_url
            if url.startswith("postgres://"):
                url = "postgresql://" + url[len("postgres://"):]
            elif url.startswith("postgresql+psycopg2://"):
                url = "postgresql://" + url[len("postgresql+psycopg2://"):]
            return psycopg2.connect(url, cursor_factory=RealDictCursor)

        connection = sqlite3.connect(_sqlite_path())
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection


database = Database()


@contextmanager
def database_connection() -> Iterator:
    connection = database.get_connection()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _consolidate_operator_role(connection) -> None:
    """Migrate the old Operador role to Supervisor without orphaning its links."""
    marker = placeholder()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, nombre FROM rol")
        role_rows = cursor.fetchall()
        roles = {
            str(row["nombre"] if isinstance(row, dict) else row[1]).strip().casefold():
                (row["id"] if isinstance(row, dict) else row[0])
            for row in role_rows
        }
        operator_id = roles.get("operador")
        supervisor_id = roles.get("supervisor")
        if operator_id is None:
            return

        description = "Gestiona asignaciones y supervisa sensores y lecturas"
        if supervisor_id is None:
            cursor.execute(
                f"UPDATE rol SET nombre = {marker}, descripcion = {marker} WHERE id = {marker}",
                ("Supervisor", description, operator_id),
            )
            return

        cursor.execute(
            f"SELECT id, idmodulo, estado FROM modulo_x_rol WHERE idrol = {marker}",
            (operator_id,),
        )
        old_permissions = cursor.fetchall()
        for row in old_permissions:
            permission_id = row["id"] if isinstance(row, dict) else row[0]
            module_id = row["idmodulo"] if isinstance(row, dict) else row[1]
            old_state = row["estado"] if isinstance(row, dict) else row[2]
            cursor.execute(
                f"SELECT id, estado FROM modulo_x_rol WHERE idrol = {marker} AND idmodulo = {marker}",
                (supervisor_id, module_id),
            )
            existing = cursor.fetchone()
            if existing is None:
                cursor.execute(
                    f"UPDATE modulo_x_rol SET idrol = {marker} WHERE id = {marker}",
                    (supervisor_id, permission_id),
                )
                continue

            existing_state = existing["estado"] if isinstance(existing, dict) else existing[1]
            existing_id = existing["id"] if isinstance(existing, dict) else existing[0]
            cursor.execute(
                f"UPDATE modulo_x_rol SET estado = {marker} WHERE id = {marker}",
                (bool(existing_state) or bool(old_state), existing_id),
            )
            cursor.execute(
                f"DELETE FROM modulo_x_rol WHERE id = {marker}",
                (permission_id,),
            )

        cursor.execute(
            f"UPDATE usuarios SET idrol = {marker} WHERE idrol = {marker}",
            (supervisor_id, operator_id),
        )
        cursor.execute(f"DELETE FROM rol WHERE id = {marker}", (operator_id,))
        cursor.execute(
            f"UPDATE rol SET descripcion = {marker} WHERE id = {marker}",
            (description, supervisor_id),
        )
    finally:
        cursor.close()


def initialize_database() -> None:
    with database_connection() as connection:
        create_schema(connection, is_postgres())
        _consolidate_operator_role(connection)
        cursor = connection.cursor()
        try:
            roles = (
                ("Administrador", "Administración de la plataforma"),
                ("Supervisor", "Gestiona asignaciones y supervisa sensores y lecturas"),
                ("Técnico", "Gestión técnica de sensores"),
            )
            marker = placeholder()
            for nombre, descripcion in roles:
                cursor.execute(
                    f"SELECT id FROM rol WHERE nombre = {marker}",
                    (nombre,),
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        f"INSERT INTO rol (nombre, descripcion, estado) VALUES ({marker}, {marker}, TRUE)",
                        (nombre, descripcion),
                    )
        finally:
            cursor.close()



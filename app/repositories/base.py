from datetime import datetime, timezone
from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from app.core.database import placeholder
from app.core.security import hash_password
from app.models.base import EntityModel


def _row_as_dict(cursor, row) -> dict[str, Any] | None:
    if row is None:
        return None
    if isinstance(row, Mapping):
        return dict(row)
    return {description[0]: row[index] for index, description in enumerate(cursor.description)}


def _db_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    return value


class BaseRepository:
    def __init__(self, entity: type[EntityModel]):
        if not isinstance(entity, type) or not issubclass(entity, EntityModel):
            raise TypeError("Repository requiere una clase de modelo Pydantic.")
        self.entity = entity

    def list(self, connection, page: int, page_size: int) -> list[dict[str, Any]]:
        marker = placeholder()
        fields = ", ".join(self.entity.read_fields())
        offset = (page - 1) * page_size
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT {fields} FROM {self.entity.table} "
                f"ORDER BY {self.entity.order_by} LIMIT {marker} OFFSET {marker}",
                (page_size, offset),
            )
            return [record for row in cursor.fetchall() if (record := _row_as_dict(cursor, row))]
        finally:
            cursor.close()

    def get(self, connection, item_id: int) -> dict[str, Any] | None:
        marker = placeholder()
        fields = ", ".join(self.entity.read_fields())
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT {fields} FROM {self.entity.table} WHERE id = {marker}",
                (item_id,),
            )
            return _row_as_dict(cursor, cursor.fetchone())
        finally:
            cursor.close()

    def create(self, connection, payload: BaseModel) -> dict[str, Any]:
        data = self.entity.payload_values(payload)
        if self.entity.table == "asignacion_sensor" and data.get("fecha_asignacion") is None:
            data["fecha_asignacion"] = datetime.now(timezone.utc)
        if self.entity.table == "lectura" and data.get("fecha_hora") is None:
            data["fecha_hora"] = datetime.now(timezone.utc)

        columns: list[str] = []
        values: list[Any] = []
        for input_name, value in data.items():
            if input_name == "password":
                value = hash_password(value)
            columns.append(input_name)
            values.append(_db_value(value))

        marker = placeholder()
        markers = ", ".join([marker] * len(columns))
        returning = ", ".join(self.entity.read_fields())
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {self.entity.table} ({', '.join(columns)}) "
                f"VALUES ({markers}) RETURNING {returning}",
                tuple(values),
            )
            return _row_as_dict(cursor, cursor.fetchone())
        finally:
            cursor.close()

    def update(self, connection, item_id: int, payload: BaseModel) -> dict[str, Any] | None:
        data = self.entity.payload_values(payload)
        changes: list[tuple[str, Any]] = []
        for input_name, value in data.items():
            if input_name == "password" and value is None:
                continue
            if input_name == "password":
                value = hash_password(value)
            changes.append((input_name, _db_value(value)))

        if not changes:
            return self.get(connection, item_id)

        marker = placeholder()
        assignments = ", ".join(f"{column} = {marker}" for column, _ in changes)
        values = [value for _, value in changes]
        values.append(item_id)
        returning = ", ".join(self.entity.read_fields())
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"UPDATE {self.entity.table} SET {assignments} "
                f"WHERE id = {marker} RETURNING {returning}",
                tuple(values),
            )
            return _row_as_dict(cursor, cursor.fetchone())
        finally:
            cursor.close()

    def delete(self, connection, item_id: int) -> bool:
        marker = placeholder()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"DELETE FROM {self.entity.table} WHERE id = {marker}",
                (item_id,),
            )
            return cursor.rowcount > 0
        finally:
            cursor.close()


# Nombre anterior conservado para evitar romper imports existentes.
Repository = BaseRepository

__all__ = ["BaseRepository", "Repository"]

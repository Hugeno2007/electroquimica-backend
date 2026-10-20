import sqlite3
import unittest
from unittest.mock import patch

from app.api.schemas import DptoCreate, DptoUpdate, UsuarioCreate
from app.core.security import verify_password
from app.models import DPTOS, USUARIOS
from app.models.schema import create_schema
from app.repositories import BaseRepository


class BaseRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        create_schema(self.connection, postgres=False)
        self.placeholder_patch = patch(
            "app.repositories.base.placeholder",
            return_value="?",
        )
        self.placeholder_patch.start()
        self.addCleanup(self.placeholder_patch.stop)
        self.addCleanup(self.connection.close)

    def test_department_create_list_update_and_delete(self):
        repository = BaseRepository(DPTOS)
        created = repository.create(
            self.connection,
            DptoCreate(nombre="Laboratorio", codigo="LAB"),
        )

        self.assertEqual(created["nombre"], "Laboratorio")
        self.assertTrue(created["estado"])
        self.assertEqual(repository.list(self.connection, page=1, page_size=10), [created])

        updated = repository.update(
            self.connection,
            created["id"],
            DptoUpdate(nombre="Laboratorio central"),
        )
        self.assertEqual(updated["nombre"], "Laboratorio central")
        self.assertTrue(repository.delete(self.connection, created["id"]))
        self.assertIsNone(repository.get(self.connection, created["id"]))
        self.assertFalse(repository.delete(self.connection, created["id"]))

    def test_user_password_is_hashed_and_omitted_from_read_data(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO rol (nombre, estado) VALUES (?, ?)",
            ("Administrador", True),
        )
        role_id = cursor.lastrowid
        cursor.close()

        password = "Temporal123!"
        created = BaseRepository(USUARIOS).create(
            self.connection,
            UsuarioCreate(
                nombre="Ana",
                apellido="Prueba",
                correo="ana@example.local",
                password=password,
                idrol=role_id,
            ),
        )

        self.assertNotIn("password", created)
        stored_hash = self.connection.execute(
            "SELECT password FROM usuarios WHERE id = ?",
            (created["id"],),
        ).fetchone()["password"]
        self.assertNotEqual(stored_hash, password)
        self.assertTrue(verify_password(password, stored_hash))


if __name__ == "__main__":
    unittest.main()

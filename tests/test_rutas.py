import sqlite3
import unittest
from contextlib import contextmanager
from unittest.mock import patch

from fastapi import FastAPI, HTTPException

from app.api import rutas_departamentos as departamentos
from app.api.rutas import api_router
from app.api.schemas import DptoCreate, DptoUpdate
from app.models.schema import create_schema


class CrudRouteTests(unittest.TestCase):
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
        self.database_patch = patch(
            "app.api.crud.database_connection",
            self._database_connection,
        )
        self.database_patch.start()
        self.addCleanup(self.database_patch.stop)
        self.addCleanup(self.connection.close)

    @contextmanager
    def _database_connection(self):
        try:
            yield self.connection
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    @staticmethod
    def _endpoint(path, method):
        return next(
            route.endpoint
            for route in departamentos.router.routes
            if route.path == path and method in route.methods
        )

    def test_all_resources_keep_the_expected_rest_routes(self):
        application = FastAPI()
        application.include_router(api_router)
        paths = application.openapi()["paths"]
        resources = (
            "/usuarios",
            "/roles",
            "/modulos",
            "/modulo-x-rol",
            "/tipos-sensor",
            "/sensores",
            "/dptos",
            "/locaciones",
            "/asignaciones-sensor",
            "/lecturas",
        )

        for path in resources:
            with self.subTest(resource=path):
                self.assertIn(path + "/", paths)
                self.assertEqual(set(paths[path + "/"]), {"get", "post"})
                self.assertIn(path + "/{item_id}", paths)
                self.assertEqual(
                    set(paths[path + "/{item_id}"]),
                    {"get", "put", "delete"},
                )

        self.assertIn("/health", paths)

    def test_department_routes_create_update_delete_and_return_404(self):
        create = self._endpoint("/dptos/", "POST")
        get = self._endpoint("/dptos/{item_id}", "GET")
        update = self._endpoint("/dptos/{item_id}", "PUT")
        delete = self._endpoint("/dptos/{item_id}", "DELETE")

        created = create(DptoCreate(nombre="Prueba", codigo="RUTA"))
        self.assertEqual(get(created["id"])["nombre"], "Prueba")

        updated = update(created["id"], DptoUpdate(nombre="Prueba editada"))
        self.assertEqual(updated["nombre"], "Prueba editada")
        self.assertIsNone(delete(created["id"]))

        with self.assertRaises(HTTPException) as error:
            get(created["id"])
        self.assertEqual(error.exception.status_code, 404)

    def test_duplicate_unique_value_returns_conflict(self):
        create = self._endpoint("/dptos/", "POST")
        create(DptoCreate(nombre="Primero", codigo="DUP"))

        with self.assertRaises(HTTPException) as error:
            create(DptoCreate(nombre="Duplicado", codigo="DUP"))
        self.assertEqual(error.exception.status_code, 409)


if __name__ == "__main__":
    unittest.main()

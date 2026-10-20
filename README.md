# ElectroQuímica API

Backend REST organizado con FastAPI y compatible con el frontend de ElectroQuímica. La estructura sigue la referencia: `app/api`, `app/core`, `app/models` y `app/repositories`.

## Requisitos

- Python 3.10 o posterior
- Las dependencias listadas en `requirements.txt`

## Instalación y ejecución

Abre PowerShell en la carpeta del backend y ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

La API queda en `http://127.0.0.1:8000`; la documentación interactiva está en `http://127.0.0.1:8000/docs`. El endpoint `/health` permite comprobar que responde.

Al iniciar, se crean las tablas y los roles Administrador, Supervisor y Técnico. Las bases existentes que tengan el rol Operador se actualizan a Supervisor conservando los usuarios y permisos asociados. El backend usa PostgreSQL cuando se configuran las variables DB_*; si no están definidas, usa SQLite local y guarda electroquimica.db en esta carpeta.

## PostgreSQL

La conexión de Neon se configura con variables separadas en `.env`:

```env
DB_HOST=TU_HOST_DE_NEON
DB_NAME=TU_BASE_DE_DATOS
DB_USER=TU_USUARIO
DB_PASSWORD=TU_CONTRASENA
DB_PORT=5432
DB_SSLMODE=require
DB_CHANNEL_BINDING=require
```

La aplicación arma la cadena de conexión a partir de esas variables. También admite `DATABASE_URL`, que tiene prioridad si está definida. No compartas ni subas `.env`; está excluido por `.gitignore`.

## Conexión del frontend

El frontend apunta por defecto a `http://127.0.0.1:8000` desde `src/lib/api.js`. Arranca Vite con `npm run dev`; la API ya permite los orígenes locales de Vite indicados en `CORS_ORIGINS`. Para cambiar la URL, define `VITE_API_URL` en el frontend.

## Rutas

Todos los recursos ofrecen `GET /`, `GET /{id}`, `POST /`, `PUT /{id}` y `DELETE /{id}`. Las listas aceptan `page` y `page_size` (máximo 100) y devuelven arreglos JSON, como espera `src/lib/api.js`.

- `/usuarios/`
- `/roles/`
- `/modulos/`
- `/modulo-x-rol/`
- `/tipos-sensor/`
- `/sensores/`
- `/dptos/`
- `/locaciones/`
- `/asignaciones-sensor/`
- `/lecturas/`

Las claves JSON corresponden a los nombres que usa `los recursos del frontend`, como `idtiposensor`, `idlocacion` y `fecha_hora`. Las tablas de base de datos usan los nombres de tu esquema: `asignacion_sensor`, `dpto`, `lectura`, `locacion`, `modulo`, `modulo_x_rol`, `rol`, `sensor`, `tipo_sensor` y `usuarios`. Las rutas HTTP se mantienen en plural donde el frontend las espera. Las relaciones y valores únicos se validan en la base de datos. Los errores por duplicados o referencias inexistentes responden con HTTP 409. La contraseña enviada al crear o actualizar un usuario se guarda como hash y no se devuelve en las respuestas.

## Nota sobre el inicio de sesión

El frontend mantiene un login de demostración en LocalStorage y no llama a una ruta de autenticación. Por eso, los permisos por perfil se aplican en la interfaz: Administrador tiene CRUD completo; Supervisor administra asignaciones y consulta los demás módulos; Técnico administra sensores, crea y consulta lecturas, y consulta los demás módulos. Las rutas CRUD de esta API no autentican ni autorizan por rol; el login de demostración no protege llamadas directas a la API.






def create_schema(connection, postgres: bool) -> None:
    id_column = "SERIAL PRIMARY KEY" if postgres else "INTEGER PRIMARY KEY AUTOINCREMENT"
    commands = [
        f"""CREATE TABLE IF NOT EXISTS rol (
            id {id_column},
            nombre VARCHAR(50) NOT NULL UNIQUE,
            descripcion VARCHAR(255),
            estado BOOLEAN NOT NULL DEFAULT TRUE
        )""",
        f"""CREATE TABLE IF NOT EXISTS modulo (
            id {id_column},
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(255),
            ruta VARCHAR(255),
            icono VARCHAR(100),
            estado BOOLEAN NOT NULL DEFAULT TRUE
        )""",
        f"""CREATE TABLE IF NOT EXISTS modulo_x_rol (
            id {id_column},
            idrol INTEGER NOT NULL REFERENCES rol(id) ON DELETE RESTRICT,
            idmodulo INTEGER NOT NULL REFERENCES modulo(id) ON DELETE RESTRICT,
            estado BOOLEAN NOT NULL DEFAULT TRUE,
            UNIQUE (idrol, idmodulo)
        )""",
        f"""CREATE TABLE IF NOT EXISTS tipo_sensor (
            id {id_column},
            nombre VARCHAR(50) NOT NULL UNIQUE,
            descripcion VARCHAR(255),
            unidad_medida VARCHAR(20) NOT NULL,
            fabricante VARCHAR(100),
            modelo VARCHAR(100),
            estado BOOLEAN NOT NULL DEFAULT TRUE
        )""",
        f"""CREATE TABLE IF NOT EXISTS dpto (
            id {id_column},
            nombre VARCHAR(100) NOT NULL,
            codigo VARCHAR(10) UNIQUE,
            estado BOOLEAN NOT NULL DEFAULT TRUE
        )""",
        f"""CREATE TABLE IF NOT EXISTS usuarios (
            id {id_column},
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            correo VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            idrol INTEGER NOT NULL REFERENCES rol(id) ON DELETE RESTRICT,
            estado BOOLEAN NOT NULL DEFAULT TRUE
        )""",
        f"""CREATE TABLE IF NOT EXISTS sensor (
            id {id_column},
            idtiposensor INTEGER NOT NULL REFERENCES tipo_sensor(id) ON DELETE RESTRICT,
            codigo VARCHAR(50) NOT NULL UNIQUE,
            nombre VARCHAR(100) NOT NULL,
            modelo VARCHAR(100),
            fabricante VARCHAR(100),
            ubicacion_fisica VARCHAR(255),
            estado BOOLEAN NOT NULL DEFAULT TRUE,
            fecha_instalacion TIMESTAMP
        )""",
        f"""CREATE TABLE IF NOT EXISTS locacion (
            id {id_column},
            iddpto INTEGER NOT NULL REFERENCES dpto(id) ON DELETE RESTRICT,
            nombre VARCHAR(100) NOT NULL,
            descripcion VARCHAR(255),
            direccion VARCHAR(255),
            latitud DOUBLE PRECISION,
            longitud DOUBLE PRECISION,
            estado BOOLEAN NOT NULL DEFAULT TRUE
        )""",
        f"""CREATE TABLE IF NOT EXISTS asignacion_sensor (
            id {id_column},
            idusuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE RESTRICT,
            idsensor INTEGER NOT NULL REFERENCES sensor(id) ON DELETE RESTRICT,
            fecha_asignacion TIMESTAMP,
            fecha_fin TIMESTAMP,
            estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVA'
                CHECK (estado IN ('ACTIVA', 'FINALIZADA'))
        )""",
        f"""CREATE TABLE IF NOT EXISTS lectura (
            id {id_column},
            idsensor INTEGER NOT NULL REFERENCES sensor(id) ON DELETE RESTRICT,
            idlocacion INTEGER NOT NULL REFERENCES locacion(id) ON DELETE RESTRICT,
            valor NUMERIC(5, 2) NOT NULL CHECK (valor >= 0 AND valor <= 14),
            temperatura NUMERIC(6, 2),
            fecha_hora TIMESTAMP NOT NULL,
            calidad VARCHAR(50)
        )""",
    ]

    cursor = connection.cursor()
    try:
        for command in commands:
            cursor.execute(command)
    finally:
        cursor.close()



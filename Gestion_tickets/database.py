import os
import sqlite3

def init_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "tickets.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabla Rol
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rol (
        id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_rol TEXT NOT NULL
    )
    """)

    cursor.execute("INSERT OR IGNORE INTO rol (id_rol, nombre_rol) VALUES (1,'Alumno')")
    cursor.execute("INSERT OR IGNORE INTO rol (id_rol, nombre_rol) VALUES (2,'Docente')")
    cursor.execute("INSERT OR IGNORE INTO rol (id_rol, nombre_rol) VALUES (3,'Administracion')")
    

    # Tabla Usuario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT UNIQUE NOT NULL,
        contraseña TEXT NOT NULL,
        id_rol INTEGER,
        FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
    )
    """)

    # Tabla Categoria
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_categoria TEXT NOT NULL
    )
    """)

    # Tabla Prioridad
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prioridad (
        id_prioridad INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_prioridad TEXT NOT NULL
    )
    """)
    cursor.execute("INSERT OR IGNORE INTO categoria (id_categoria, nombre_categoria) VALUES (1,'Infraestructura')")
    cursor.execute("INSERT OR IGNORE INTO categoria (id_categoria, nombre_categoria) VALUES (2,'Servicios')")
    cursor.execute("INSERT OR IGNORE INTO categoria (id_categoria, nombre_categoria) VALUES (3,'Docencia')")
    cursor.execute("INSERT OR IGNORE INTO categoria (id_categoria, nombre_categoria) VALUES (4,'Administrativo')")

    cursor.execute("INSERT OR IGNORE INTO prioridad VALUES (1,'Baja')")
    cursor.execute("INSERT OR IGNORE INTO prioridad VALUES (2,'Media')")
    cursor.execute("INSERT OR IGNORE INTO prioridad VALUES (3,'Alta')")

    # Tabla Estado
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estado (
        id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_estado TEXT NOT NULL
    )
    """)

    cursor.execute("INSERT OR IGNORE INTO estado VALUES (1,'Pendiente')")
    cursor.execute("INSERT OR IGNORE INTO estado VALUES (2,'En proceso')")
    cursor.execute("INSERT OR IGNORE INTO estado VALUES (3,'Resuelto')")

    # Tabla Departamento
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departamento (
        id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_departamento TEXT NOT NULL
    )
    """)

    # Tabla Ticket
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket (
        id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        fecha_creacion TEXT,
        id_usuario INTEGER,
        id_categoria INTEGER,
        id_prioridad INTEGER,
        id_estado INTEGER,
        id_departamento INTEGER,
        ruta_imagen TEXT,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
        FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
        FOREIGN KEY (id_prioridad) REFERENCES prioridad(id_prioridad),
        FOREIGN KEY (id_estado) REFERENCES estado(id_estado),
        FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
    )
    """)

    # Tabla Historial de cambios del ticket
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_ticket (
        id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
        id_ticket INTEGER,
        id_estado INTEGER,
        fecha_cambio TEXT,
        comentario TEXT,
        FOREIGN KEY (id_ticket) REFERENCES ticket(id_ticket),
        FOREIGN KEY (id_estado) REFERENCES estado(id_estado)
    )
    """)
    # Agregar columna comentario_admin si no existe
    try:
        cursor.execute("ALTER TABLE ticket ADD COLUMN comentario_admin TEXT")
    except:
       pass
    conn.commit()
    conn.close()

   

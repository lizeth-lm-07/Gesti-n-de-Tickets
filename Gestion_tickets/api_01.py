import sqlite3
from sqlite3 import Error
import os
from datetime import datetime

class Database:
    
    def __init__(self, db_file):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(base_dir, db_file)
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def login(self, correo, contraseña):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, id_rol FROM usuario WHERE correo = ? AND contraseña = ?",
            (correo, contraseña)
        )
        user = cursor.fetchone()
        self.disconnect()
        return user  

    def buscar_usuario(self, correo):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = ?", (correo,))
        user = cursor.fetchone()
        self.disconnect()
        return user

    def registrar_usuario(self, nombre, correo, contrasena, tipo):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, correo, contraseña, id_rol) VALUES (?, ?, ?, ?)",
            (nombre, correo, contrasena, tipo)
        )
        self.conn.commit()
        self.disconnect()

    def obtener_usuario_por_id(self, id_usuario):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, correo, id_rol FROM usuario WHERE id_usuario = ?",
            (id_usuario,)
        )
        user = cursor.fetchone()
        self.disconnect()
        return user

    # 🔥 YA TRAE IMAGEN
    def obtener_todos_tickets(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.id_ticket, u.nombre, c.nombre_categoria,
                   p.nombre_prioridad, e.nombre_estado,
                   t.fecha_creacion, t.ruta_imagen
            FROM ticket t
            LEFT JOIN usuario u ON t.id_usuario = u.id_usuario
            LEFT JOIN categoria c ON t.id_categoria = c.id_categoria
            LEFT JOIN prioridad p ON t.id_prioridad = p.id_prioridad
            LEFT JOIN estado e ON t.id_estado = e.id_estado
            ORDER BY t.fecha_creacion DESC
        """)
        tickets = cursor.fetchall()
        self.disconnect()
        return tickets

    # 🔥 CORREGIDO
    def crear_ticket(self, titulo, descripcion, id_categoria, id_prioridad, id_usuario, ruta_imagen):
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO ticket (
                titulo, descripcion, fecha_creacion,
                id_usuario, id_categoria, id_prioridad,
                id_estado, id_departamento, ruta_imagen
            )
            VALUES (?, ?, datetime('now'), ?, ?, ?, 1, ?, ?)
        """, (
            titulo,
            descripcion,
            id_usuario,
            id_categoria,
            id_prioridad,
            id_categoria,
            ruta_imagen
        ))

        self.conn.commit()
        self.disconnect()

    def obtener_categorias(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_categoria, nombre_categoria FROM categoria")
        categorias = cursor.fetchall()
        self.disconnect()
        return categorias

    def obtener_prioridades(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_prioridad, nombre_prioridad FROM prioridad")
        prioridades = cursor.fetchall()
        self.disconnect()
        return prioridades

    def obtener_tickets_usuario(self, id_usuario):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.id_ticket, t.titulo, t.fecha_creacion,
                   c.nombre_categoria, e.nombre_estado, t.comentario_admin
            FROM ticket t
            LEFT JOIN categoria c ON t.id_categoria = c.id_categoria
            LEFT JOIN estado e ON t.id_estado = e.id_estado
            WHERE t.id_usuario = ?
            ORDER BY t.fecha_creacion DESC
        """, (id_usuario,))
        tickets = cursor.fetchall()
        self.disconnect()
        return tickets

    def obtener_ticket_detalle(self, id_ticket):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.id_ticket, u.nombre, c.nombre_categoria,
                   p.nombre_prioridad, e.nombre_estado, t.fecha_creacion,
                   t.titulo, t.descripcion, t.ruta_imagen, t.id_estado,
                   t.comentario_admin
            FROM ticket t
            LEFT JOIN usuario u ON t.id_usuario = u.id_usuario
            LEFT JOIN categoria c ON t.id_categoria = c.id_categoria
            LEFT JOIN prioridad p ON t.id_prioridad = p.id_prioridad
            LEFT JOIN estado e ON t.id_estado = e.id_estado
            WHERE t.id_ticket = ?
        """, (id_ticket,))
        ticket = cursor.fetchone()
        self.disconnect()
        return ticket

    def obtener_estados(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_estado, nombre_estado FROM estado")
        estados = cursor.fetchall()
        self.disconnect()
        return estados

    def actualizar_estado_ticket(self, id_ticket, id_estado, comentario_admin=None):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE ticket SET id_estado = ?, comentario_admin = ? WHERE id_ticket = ?",
            (id_estado, comentario_admin, id_ticket)
        )
        self.conn.commit()
        self.disconnect()

    def obtener_responsables(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT r.id_responsable, r.cargo, d.nombre_departamento, r.correo, r.telefono
            FROM responsable r
            LEFT JOIN departamento d ON r.id_departamento = d.id_departamento
        """)
        responsables = cursor.fetchall()
        self.disconnect()
        return responsables
    
    def obtener_departamentos(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_departamento, nombre_departamento FROM departamento")
        departamentos = cursor.fetchall()
        self.disconnect()
        return departamentos
    
    def agregar_responsable(self, cargo, id_departamento, correo, telefono):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO responsable (cargo, id_departamento, correo, telefono)
            VALUES (?, ?, ?, ?)
        """, (cargo, id_departamento, correo, telefono))
        self.conn.commit()
        self.disconnect()

    def editar_responsable(self, id_responsable, cargo, id_departamento, correo, telefono):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE responsable
            SET cargo = ?, id_departamento = ?, correo = ?, telefono = ?
            WHERE id_responsable = ?
        """, (cargo, id_departamento, correo, telefono, id_responsable))
        self.conn.commit()
        self.disconnect()

    def obtener_responsable_por_id(self, id_responsable):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id_responsable, cargo, id_departamento, correo, telefono
            FROM responsable
            WHERE id_responsable = ?
        """, (id_responsable,))
        responsable = cursor.fetchone()
        self.disconnect()
        return responsable
    
    def eliminar_responsable(self, id_responsable):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM responsable WHERE id_responsable = ?", (id_responsable,))
        self.conn.commit()
        self.disconnect()
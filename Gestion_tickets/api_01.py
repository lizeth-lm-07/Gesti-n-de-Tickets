import sqlite3
from sqlite3 import Error

import os


class Database:

    def __init__(self, db_file):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(base_dir, db_file)
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("Conexión a la base de datos establecida.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def login(self, correo, contraseña):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, id_rol FROM usuario WHERE correo = ? AND contraseña = ?",
            (correo, contraseña)
        )
        user = cursor.fetchone()
        self.disconnect()
        return user  # Devuelve None si no se encuentra el usuario
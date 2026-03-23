import sqlite3
import os

import api_01 as api

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "tickets.db")

api_db = api.Database(db_path)

api.Database.crear_ticket(api_db, "Título de prueba", "Descripción de prueba", 1, 1, 1)

with sqlite3.connect(db_path) as conn:
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM usuario")
	print(cursor.fetchall())
	pass  # Connection will be closed automatically



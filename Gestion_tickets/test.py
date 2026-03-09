import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "tickets.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM usuario")
print(cursor.fetchall())
conn.close()
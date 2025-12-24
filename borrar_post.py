import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

id_a_borrar = 10  # ← CAMBIA ESTE POR EL ID REAL DEL DUPLICADO

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DELETE FROM posts WHERE id = ?", (id_a_borrar,))
conn.commit()

print(f"Post con ID {id_a_borrar} eliminado correctamente.")
conn.close()
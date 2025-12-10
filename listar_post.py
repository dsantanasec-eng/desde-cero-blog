from pathlib import Path
import sqlite3

# Ruta a la base de datos (igual que en main.py)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT id, date, slug, title FROM posts ORDER BY date DESC")

print("ID | FECHA               | SLUG                              | TÍTULO")
print("-" * 90)
for row in cur.fetchall():
    print(f"{row['id']:2} | {row['date']:19} | {row['slug'][:30]:30} | {row['title']}")
conn.close()
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# DB vieja: la que está en el repo / proyecto
OLD_DB = BASE_DIR / "mi_blog.db"

# DB nueva: la que usa el main.py (DATA_DIR o /tmp)
DATA_DIR = Path(__import__("os").environ.get("DATA_DIR", "/tmp"))
NEW_DB = DATA_DIR / "mi_blog.db"

def ensure_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            slug    TEXT NOT NULL UNIQUE,
            date    TEXT NOT NULL,
            tags    TEXT,
            excerpt TEXT,
            content TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id   INTEGER NOT NULL,
            author    TEXT NOT NULL,
            text      TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        )
    """)
    conn.commit()

def migrate():
    if not OLD_DB.exists():
        raise FileNotFoundError(f"No encuentro la DB vieja: {OLD_DB}")

    NEW_DB.parent.mkdir(parents=True, exist_ok=True)

    old = sqlite3.connect(OLD_DB)
    old.row_factory = sqlite3.Row

    new = sqlite3.connect(NEW_DB)
    new.row_factory = sqlite3.Row

    ensure_tables(new)

    old_cur = old.cursor()
    new_cur = new.cursor()

    # Copiar posts
    old_cur.execute("SELECT title, slug, date, tags, excerpt, content FROM posts")
    posts = old_cur.fetchall()

    copied = 0
    for p in posts:
        try:
            new_cur.execute("""
                INSERT INTO posts (title, slug, date, tags, excerpt, content)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (p["title"], p["slug"], p["date"], p["tags"], p["excerpt"], p["content"]))
            copied += 1
        except sqlite3.IntegrityError:
            # slug duplicado, lo saltamos
            pass

    # Copiar comments (si existen)
    try:
        old_cur.execute("SELECT post_id, author, text, created_at FROM comments")
        comments = old_cur.fetchall()
        for c in comments:
            new_cur.execute("""
                INSERT INTO comments (post_id, author, text, created_at)
                VALUES (?, ?, ?, ?)
            """, (c["post_id"], c["author"], c["text"], c["created_at"]))
    except sqlite3.OperationalError:
        # si la tabla no existe en la vieja, ignoramos
        pass

    new.commit()
    old.close()
    new.close()

    print(f"✅ Migración lista. Posts copiados: {copied}")
    print(f"📦 Nueva DB en: {NEW_DB}")

if __name__ == "__main__":
    migrate()
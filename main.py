import argparse
import sqlite3
from pathlib import Path
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    abort,
)

# ---------------- Configuración básica ----------------

app = Flask(__name__)

# Ruta al archivo de base de datos (mi_blog.db en la carpeta del proyecto)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"


# --------------- Conexión y helpers de BD ---------------

def get_conn():
    """Devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder por nombre de columna
    return conn


def init_db(seed=False):
    """
    Crea las tablas si no existen.
    Si seed=True y no hay posts, inserta un post de ejemplo.
    """
    conn = get_conn()
    cur = conn.cursor()

    # Tabla de posts
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            slug    TEXT NOT NULL UNIQUE,
            date    TEXT NOT NULL,      -- formato ISO 'YYYY-MM-DD HH:MM:SS'
            tags    TEXT,
            excerpt TEXT,
            content TEXT NOT NULL
        )
        """
    )

    # Tabla de comentarios
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id   INTEGER NOT NULL,
            author    TEXT NOT NULL,
            text      TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()

    # Semilla: crear 1 post de ejemplo si no hay ninguno
    if seed:
        cur.execute("SELECT COUNT(*) FROM posts")
        count = cur.fetchone()[0]

        if count == 0:
            content_html = """
<p>He probado muchos cursos de Python y estos son los 5 que de verdad recomiendo si estás empezando desde cero:</p>

<ol>
  <li><strong>Google IT Automation with Python (Coursera)</strong><br>
      Ideal si quieres usar Python para automatizar tareas de soporte técnico y sistemas.
  </li>
  <li><strong>Python for Everybody (Coursera)</strong><br>
      Muy bueno para entender bien las bases de Python sin ir demasiado rápido.
  </li>
  <li><strong>Automate the Boring Stuff with Python</strong><br>
      Perfecto si quieres ver ejemplos prácticos para automatizar cosas reales en tu PC.
  </li>
  <li><strong>CS50P – Introduction to Programming with Python (Harvard / edX)</strong><br>
      Más completo y un poco más exigente, pero te da una base fuerte de programación.
  </li>
  <li><strong>FreeCodeCamp | Python / Backend</strong><br>
      Gratis y con muchos ejercicios para practicar y reforzar.
  </li>
</ol>

<p>Mi consejo: elige <strong>uno</strong> para empezar, termínalo, y mientras tanto ve construyendo mini proyectos sencillos. Después puedes pasar al siguiente.</p>
"""

            cur.execute(
                """
                INSERT INTO posts (title, slug, date, tags, excerpt, content)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    "Top 5 cursos gratuitos para aprender Python",
                    "cursos-gratis-python-desde-cero",
                    "2025-11-10 00:00:00",
                    "python, educación",
                    "Mi selección de cursos online gratuitos que realmente valen la pena si estás empezando desde cero.",
                    content_html.strip(),
                ),
            )
            conn.commit()
            print("✔ Se creó el post de ejemplo en la base de datos.")

    conn.close()


def get_all_posts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_post_by_slug(slug: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()
    return row


def get_comments(post_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM comments WHERE post_id = ? ORDER BY created_at DESC",
        (post_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def add_comment(post_id: int, author: str, text: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO comments (post_id, author, text, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            post_id,
            author,
            text,
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    conn.close()


# ---------------- Filtros y contexto global ----------------

@app.template_filter("fecha")
def formato_fecha(value):
    """
    Convierte una fecha tipo string 'YYYY-MM-DD HH:MM:SS' a 'DD/MM/YYYY HH:MM'.
    Si ya viene como datetime o algo raro, intentamos y si falla la dejamos igual.
    """
    try:
        if isinstance(value, str):
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        else:
            dt = value
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return value


@app.context_processor
def inject_globals():
    """Variables disponibles en todos los templates."""
    now = datetime.utcnow()
    return {
        "now": now,
        "current_year": now.year,
        "site_name": "Desde Cero",
    }


# ---------------------- Rutas ---------------------------

@app.route("/")
def home():
    posts = get_all_posts()
    last_post = posts[0] if posts else None
    return render_template("index.html", post=last_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog")
def blog_list():
    posts = get_all_posts()
    return render_template("blog_list.html", posts=posts)


@app.route("/post/<slug>", methods=["GET", "POST"])
def post_detail(slug):
    post = get_post_by_slug(slug)
    if not post:
        abort(404)

    if request.method == "POST":
        author = request.form.get("author", "").strip()
        text = request.form.get("text", "").strip()

        if author and text:
            add_comment(post["id"], author, text)
            return redirect(url_for("post_detail", slug=slug))

    comments = get_comments(post["id"])
    return render_template("post_detail.html", post=post, comments=comments)


# ----------------- Arranque / CLI -----------------------

def main():
    parser = argparse.ArgumentParser(description="Blog 'Desde Cero'")
    parser.add_argument(
        "--initdb",
        action="store_true",
        help="Crear/sembrar la base de datos (elimina la anterior si la borraste)",
    )
    args = parser.parse_args()

    if args.initdb:
        print("Inicializando base de datos en:", DB_PATH)
        init_db(seed=True)
        print("✔ Base de datos lista.")
    else:
        app.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
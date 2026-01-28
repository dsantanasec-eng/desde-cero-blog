import argparse
import sqlite3
from pathlib import Path
from datetime import datetime
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    send_file,
    flash,
    send_from_directory,
)

# ---------------- Configuración básica ----------------

app = Flask(__name__)

# Secret para flash/messages (Render usa env var, local usa fallback)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# Admin ON/OFF (cuando termines de publicar posts, ponlo en False y haces push)
ADMIN_ENABLED = True
ADMIN_KEY = os.environ.get("ADMIN_KEY", "desde-cero-admin")

# Ruta al archivo de base de datos (mi_blog.db en la carpeta del proyecto)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

# ---------------- Redirect www -> non-www ----------------

@app.before_request
def redirect_www():
    if request.host.startswith("www."):
        return redirect(request.url.replace("www.", "", 1), code=301)

# --------------- Conexión y helpers de BD ---------------

def get_conn():
    """Devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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

    if seed:
        cur.execute("SELECT COUNT(*) FROM posts")
        count = cur.fetchone()[0]

        if count == 0:
            content_html = """
<p>He probado muchos cursos de Python y estos son los 5 que de verdad recomiendo si estás empezando desde cero:</p>
<ol>
  <li><strong>Google IT Automation with Python (Coursera)</strong></li>
  <li><strong>Python for Everybody (Coursera)</strong></li>
  <li><strong>Automate the Boring Stuff with Python</strong></li>
  <li><strong>CS50P – Introduction to Programming with Python (Harvard / edX)</strong></li>
  <li><strong>FreeCodeCamp | Python / Backend</strong></li>
</ol>
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

    conn.close()


# ✅ IMPORTANTE: en Render la DB puede venir vacía.
# Esto asegura que existan las tablas siempre (no mete posts, solo crea tablas).
try:
    init_db(seed=False)
except Exception as e:
    print("⚠️ No pude inicializar la DB automáticamente:", e)


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
        (post_id, author, text, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


# ---------------- Contexto global ----------------

@app.context_processor
def inject_globals():
    now = datetime.utcnow()
    return {"now": now, "current_year": now.year, "site_name": "Desde Cero"}


# ---------------------- Rutas ---------------------------

@app.route("/")
def home():
    posts = get_all_posts()
    last_post = posts[0] if posts else None
    fecha = datetime.now().strftime("%d/%m/%Y")
    return render_template("index.html", post=last_post, fecha=fecha)


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


# ✅ ADMIN para crear posts desde la web:
# URL: /admin?key=TUCLAVE
@app.route("/admin", methods=["GET", "POST"])
def admin_new():
    if not ADMIN_ENABLED:
        abort(404)

    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        abort(403)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip()
        tags = request.form.get("tags", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not slug or not content:
            flash("Faltan campos obligatorios: título, slug y contenido.")
            return redirect(url_for("admin_new", key=ADMIN_KEY))

        created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO posts (title, slug, date, tags, excerpt, content)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, slug, created_at, tags, excerpt, content),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash("Ese slug ya existe. Cámbialo por uno diferente.")
            return redirect(url_for("admin_new", key=ADMIN_KEY))

        conn.close()
        flash("✅ Post publicado.")
        return redirect(url_for("blog_list"))

    return render_template("admin_new.html")


# ----------- sitemap.xml ----------------
@app.route("/sitemap.xml")
def sitemap():
    return send_file(
        os.path.join(BASE_DIR, "sitemap.xml"),
        mimetype="application/xml",
        as_attachment=False
    )


# ----------- robots.txt ----------------
@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", now=datetime.utcnow())


@app.route("/terms")
def terms():
    return render_template("terms.html", now=datetime.utcnow())


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ----------------- Arranque / CLI -----------------------

def main():
    parser = argparse.ArgumentParser(description="Blog 'Desde Cero'")
    parser.add_argument("--initdb", action="store_true", help="Crear/sembrar la base de datos")
    args = parser.parse_args()

    if args.initdb:
        print("Inicializando base de datos en:", DB_PATH)
        init_db(seed=True)
        print("✔ Base de datos lista.")
    else:
        app.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
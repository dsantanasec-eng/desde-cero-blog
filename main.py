import sqlite3
from pathlib import Path
from datetime import datetime, date
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    send_file,
    send_from_directory,
)

app = Flask(__name__)

# ---------------- Configuración ----------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

# ---------------- Redirect www ----------------

@app.before_request
def redirect_www():
    if request.host.startswith("www."):
        return redirect(request.url.replace("www.", "", 1), code=301)

# ---------------- DB helpers ----------------

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            date TEXT NOT NULL,
            tags TEXT,
            excerpt TEXT,
            content TEXT NOT NULL
        )
    """)

    conn.commit()

    # 🔥 SEED AUTOMÁTICO (solo si no hay posts)
    cur.execute("SELECT COUNT(*) FROM posts")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO posts (title, slug, date, tags, excerpt, content)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Por qué decidí aprender C++ y cómo ha sido el proceso hasta ahora",
            "por-que-aprender-cpp-y-como-ha-sido-mi-proceso",
            date.today().isoformat(),
            "c++,programacion,aprendizaje",
            "Quería entender qué pasa por debajo del código. C++ me obligó a pensar distinto.",
            """Durante mucho tiempo pensé que aprender a programar era solo elegir un lenguaje popular y ya...

(PEGA AQUÍ EL CONTENIDO COMPLETO DEL POST)
"""
        ))
        conn.commit()
        print("✔ Post inicial creado en producción")

    conn.close()


# ---------------- Filters ----------------

@app.template_filter("fecha")
def formato_fecha(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return value


@app.context_processor
def inject_globals():
    now = datetime.utcnow()
    return {
        "current_year": now.year,
        "site_name": "Desde Cero",
    }

# ---------------- Routes ----------------

@app.route("/")
def home():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY date DESC LIMIT 1")
    post = cur.fetchone()
    conn.close()
    return render_template("index.html", post=post)


@app.route("/blog")
def blog_list():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY date DESC")
    posts = cur.fetchall()
    conn.close()
    return render_template("blog_list.html", posts=posts)


@app.route("/post/<slug>")
def post_detail(slug):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE slug = ?", (slug,))
    post = cur.fetchone()
    conn.close()

    if not post:
        abort(404)

    return render_template("post_detail.html", post=post)


@app.route("/sitemap.xml")
def sitemap():
    return send_file(BASE_DIR / "sitemap.xml", mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")


# ---------------- RUN ----------------

if __name__ == "_main_":
    init_db()  # 🔥 ESTO ES LA CLAVE
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
import argparse
import os
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
    send_file,
    send_from_directory,
    session,
    flash,
)

# ---------------- Configuración básica ----------------

app = Flask(__name__)

# ✅ Necesario para session/flash (ponlo en Render como env var SECRET_KEY)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

BASE_DIR = Path(__file__).resolve().parent

# ✅ Render: SQLite suele fallar si intentas escribir en el root del repo.
# Guardamos la DB en un directorio escribible.
# - Local: DATA_DIR puede ser el proyecto si quieres
# - Render: por defecto /tmp (writable)
DATA_DIR = Path(os.environ.get("DATA_DIR", "/tmp"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "mi_blog.db"


# -------------------- Redirect www --------------------

@app.before_request
def redirect_www():
    # si llega por www, lo mandamos a sin www
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
            date    TEXT NOT NULL,      -- 'YYYY-MM-DD HH:MM:SS'
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
""".strip()

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
                    content_html,
                ),
            )
            conn.commit()

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


def add_post(title: str, slug: str, tags: str, excerpt: str, content: str):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO posts (title, slug, date, tags, excerpt, content)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, slug, now, tags, excerpt, content),
    )
    conn.commit()
    conn.close()


# ✅ Render: inicializa DB automáticamente al arrancar
try:
    init_db(seed=False)
except Exception as e:
    print("⚠️ No pude inicializar la DB automáticamente:", e)


# ---------------- Filtros y contexto global ----------------

@app.template_filter("fecha")
def formato_fecha(value):
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
    now = datetime.utcnow()
    return {
        "now": now,
        "current_year": now.year,
        "site_name": "Desde Cero",
    }


# ---------------------- Rutas públicas ---------------------------

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


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", now=datetime.utcnow())


@app.route("/terms")
def terms():
    return render_template("terms.html", now=datetime.utcnow())


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- SEO: robots + sitemap ----------------

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    return send_file(
        os.path.join(BASE_DIR, "sitemap.xml"),
        mimetype="application/xml",
        as_attachment=False,
    )


# ---------------- Admin (crear posts desde la web) ----------------
# ✅ Para no “exponer” admin, lo puedes apagar con ADMIN_ENABLED=0
ADMIN_ENABLED = os.environ.get("ADMIN_ENABLED", "1") == "1"

# ✅ Token simple (ponlo en Render como env var ADMIN_TOKEN)
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

def admin_is_logged_in():
    return session.get("is_admin") is True


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if not ADMIN_ENABLED:
        abort(404)

    if request.method == "POST":
        token = request.form.get("token", "").strip()

        if ADMIN_TOKEN and token == ADMIN_TOKEN:
            session["is_admin"] = True
            flash("✅ Admin activado.", "success")
            return redirect(url_for("admin_new"))
        else:
            flash("❌ Token incorrecto.", "error")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    if not ADMIN_ENABLED:
        abort(404)
    session.pop("is_admin", None)
    flash("✅ Sesión cerrada.", "success")
    return redirect(url_for("home"))


@app.route("/admin/new", methods=["GET", "POST"])
def admin_new():
    if not ADMIN_ENABLED:
        abort(404)

    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip()
        tags = request.form.get("tags", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not slug or not content:
            flash("⚠️ Title, Slug y Content son obligatorios.", "error")
            return render_template("admin_new.html")

        try:
            add_post(title, slug, tags, excerpt, content)
            flash("✅ Post publicado.", "success")
            return redirect(url_for("post_detail", slug=slug))
        except sqlite3.IntegrityError:
            flash("❌ Ese slug ya existe. Usa otro.", "error")
        except Exception as e:
            flash(f"❌ Error guardando post: {e}", "error")

    return render_template("admin_new.html")


# ----------------- Arranque / CLI -----------------------

def main():
    parser = argparse.ArgumentParser(description="Blog 'Desde Cero'")
    parser.add_argument(
        "--initdb",
        action="store_true",
        help="Crear/sembrar la base de datos (solo local)",
    )
    args = parser.parse_args()

    if args.initdb:
        print("Inicializando base de datos en:", DB_PATH)
        init_db(seed=True)
        print("✔ Base de datos lista.")
    else:
        # Local
        app.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
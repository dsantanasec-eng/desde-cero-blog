from datetime import datetime
import sqlite3
from pathlib import Path

# Ruta exacta a tu base de datos SQLite
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # ---- DATOS DEL NUEVO POST ----
    title = "Why Learning Python in 2026 Can Change Your Life (U.S. Guide)"
    slug = "python-career-guide-usa-2026"
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    tags = "python, beginners, career, usa, english"

    excerpt = (
        "A clear and practical guide for U.S. beginners who want to start a tech career "
        "using Python in 2026 — even with no prior experience."
    )

    content_html = """
    <h2>Start Your Python Journey in 2026</h2>
    <p>If you're in the United States and want a real opportunity to start a new career, Python is one of the best choices.</p>

    <h3>Why Python?</h3>
    <ul>
      <li>Easy to learn and beginner friendly</li>
      <li>High demand in tech companies</li>
      <li>Remote job opportunities</li>
      <li>High salaries starting from $55,000 to $120,000</li>
    </ul>

    <h3>Step-by-step plan</h3>
    <ol>
      <li>Learn Python basics (4–6 weeks)</li>
      <li>Build 3–5 small projects</li>
      <li>Create your GitHub portfolio</li>
      <li>Learn SQL + basic Linux</li>
      <li>Apply for internships, entry-level roles, or freelance work</li>
    </ol>

    <p>Consistency beats talent. Start today and your life can look completely different within one year.</p>

    <h3>Final Advice</h3>
    <p>No degree? No problem. The tech industry cares more about skills than diplomas.</p>
    """

    # ---- INSERTAR EN LA BASE DE DATOS ----
    cur.execute("""
        INSERT INTO posts (title, slug, date, tags, excerpt, content_html)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, slug, date_str, tags, excerpt, content_html.strip()))

    conn.commit()
    conn.close()

    print("📌 Nuevo post agregado correctamente:", title)

if __name__ == "__main__":
    main()
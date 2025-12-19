import sqlite3
from pathlib import Path
from datetime import datetime

# Database path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    title = "Why Learning Basic HTML Still Matters in 2025"
    slug = "why-learning-basic-html-still-matters-2025"  # MUST BE UNIQUE
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tags = "html, web development, beginners, usa, programming"
    excerpt = (
        "HTML is still the foundation of the web. Understanding it gives you "
        "an advantage when learning programming, web development, or tech careers."
    )

    content_html = """
    <h2>HTML Is the Foundation of the Web</h2>
    <p>
    Every website you visit, every landing page, every blog, and even many apps
    start with HTML. While modern tools exist, HTML remains essential knowledge.
    </p>

    <h2>Why This Matters in the U.S. Tech Market</h2>
    <p>
    In the United States, many entry-level tech roles expect at least a basic
    understanding of HTML. It helps you communicate with developers, designers,
    and understand how the web actually works.
    </p>

    <h2>HTML Helps You Learn Faster</h2>
    <p>
    When you understand HTML, learning CSS, JavaScript, and even backend
    frameworks becomes much easier. You stop guessing and start building.
    </p>

    <h2>Final Thought</h2>
    <p>
    You don’t need to master HTML, but learning the basics is one of the smartest
    moves you can make if you want to grow in tech in 2025.
    </p>
    """

    cur.execute("""
        INSERT INTO posts (title, slug, date, tags, excerpt, content_html)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, slug, date_str, tags, excerpt, content_html.strip()))

    conn.commit()
    conn.close()

    print("✅ Post inserted successfully.")

if __name__ == "__main__":
    main()
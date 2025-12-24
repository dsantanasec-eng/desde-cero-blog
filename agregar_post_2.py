import os
import sqlite3
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), "mi_blog.db")


def make_unique_slug(cur, base_slug: str) -> str:
    """
    If base_slug exists, returns base_slug-2, base_slug-3, etc.
    """
    slug = base_slug.strip().lower()
    n = 1
    while True:
        cur.execute("SELECT 1 FROM posts WHERE slug = ? LIMIT 1", (slug,))
        exists = cur.fetchone()
        if not exists:
            return slug
        n += 1
        slug = f"{base_slug}-{n}"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ====== EDITA SOLO ESTO (si quieres cambiar el post) ======
    title = "How to Train Your Programming Logic (Even If You’re Just Starting)"
    base_slug = "how-to-train-programming-logic-beginners"  # este es el que te está chocando
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tags = "programming logic, beginners, problem solving, coding mindset, usa"
    excerpt = (
        "Programming is not about memorizing syntax. It’s about learning how to think. "
        "Here are practical ways to train your programming logic from day one."
    )

    content = """
<p>One of the biggest mistakes beginners make is thinking that programming is about learning a language.</p>
<p>It’s not.</p>

<p>Programming is about learning how to <strong>think</strong>. Languages are just tools.</p>

<h2>1) Solve tiny problems daily (10–20 minutes)</h2>
<p>Pick one small problem per day: reverse a string, count vowels, find the max number, remove duplicates, etc.
Small problems build consistency and confidence.</p>

<h2>2) Say your logic out loud before coding</h2>
<p>Before touching the keyboard, explain the steps like you’re teaching someone:
“What do I know? What do I need? What should happen next?”</p>

<h2>3) Write the steps as plain English first</h2>
<p>Example: “Read the numbers → keep the biggest → print it.” Then translate to code.</p>

<h2>4) Get comfortable with loops + conditions</h2>
<p>If you understand <strong>if</strong> and <strong>for/while</strong>, you can build almost anything.
Most beginner problems are just loops + decisions.</p>

<h2>5) Debug like a detective</h2>
<ul>
  <li>Print variables.</li>
  <li>Check one step at a time.</li>
  <li>Ask: “What did I expect vs what happened?”</li>
</ul>

<h2>6) Repeat patterns (not tutorials)</h2>
<p>Tutorials feel productive, but repetition is what makes you improve.
Solve the same type of problem in 3 different ways.</p>

<h2>Final thought</h2>
<p>Your logic improves every time you struggle and keep going. That’s the game.</p>
"""
    # ===========================================================

    # Crear slug único
    slug = make_unique_slug(cur, base_slug)

    cur.execute(
        """
        INSERT INTO posts (title, slug, date, tags, excerpt, content)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, slug, date_str, tags, excerpt, content.strip()),
    )

    conn.commit()
    conn.close()

    print("✅ Post added successfully.")
    print(f"✅ Slug usado: {slug}")


if __name__ == "__main__":
    main()
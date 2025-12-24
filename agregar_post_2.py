import sqlite3
from pathlib import Path
from datetime import datetime

# Ruta a la base de datos
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    title = "How to Train Your Programming Logic (Even If You’re Just Starting)"
    slug = "how-to-train-programming-logic-beginners"
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

<h2>1. Stop Trying to Memorize Code</h2>
<p>
If you try to memorize syntax, you will feel stuck very fast.  
Instead, focus on understanding <em>why</em> a solution works.
</p>

<p>
Ask yourself questions like:
</p>
<ul>
  <li>What problem am I solving?</li>
  <li>What information do I already have?</li>
  <li>What needs to happen step by step?</li>
</ul>

<h2>2. Break Problems Into Small Pieces</h2>
<p>
Good programmers don’t solve big problems at once.  
They break them into tiny, manageable steps.
</p>

<p>
If a task feels overwhelming, it means it’s still too big.
</p>

<h2>3. Think in Plain English First</h2>
<p>
Before writing code, explain the solution in simple words.
</p>

<p>
If you can explain the logic clearly in English, writing the code becomes much easier.
</p>

<h2>4. Practice With Simple Exercises</h2>
<p>
You don’t need complex projects to train your logic.
</p>

<p>
Simple exercises like:
</p>
<ul>
  <li>Checking if a number is even or odd</li>
  <li>Finding the largest value in a list</li>
  <li>Simulating real-life decisions with conditions</li>
</ul>

<p>
These build strong fundamentals.
</p>

<h2>5. Struggle Is Part of the Process</h2>
<p>
Feeling confused doesn’t mean you’re bad at programming.
</p>

<p>
It means your brain is learning a new way of thinking.
</p>

<p>
Every programmer you admire went through this phase.
</p>

<h2>Final Thought</h2>
<p>
If you focus on training your logic instead of rushing to learn frameworks,
you’ll progress faster and feel more confident long-term.
</p>

<p>
Programming is a skill — and skills are built one step at a time.
</p>
"""

    cur.execute("""
        INSERT INTO posts (title, slug, date, tags, excerpt, content)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, slug, date_str, tags, excerpt, content.strip()))

    conn.commit()
    conn.close()

    print("✅ Post added successfully.")

if __name__ == "__main__":
    main()
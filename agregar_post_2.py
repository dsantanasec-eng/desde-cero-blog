from datetime import datetime
import sqlite3
from pathlib import Path

# Ruta a la base de datos (igual que en main.py)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    title = "How to start your Python career in 2026 (step-by-step guide)"
    slug = "python-career-2026-step-by-step"
    date_str = "2025-12-03 00:00:00"  # puedes cambiar la fecha si quieres
    tags = "python, career, beginners, english, usa"

    excerpt = (
        "A clear step-by-step roadmap to go from zero to your first Python job "
        "or freelance income in 2026, without getting stuck or overwhelmed."
    )

    content_html = """
<h2>Why Python is still a great bet for 2026</h2>
<p>
Python is not “dead” and it’s not “too saturated”. It’s a mature, flexible
language that companies use for automation, data, backend, AI and more.
If you are starting from zero and want a realistic way to enter tech, Python
is still one of the best doors.
</p>

<h2>Step 1: Choose one clear goal</h2>
<p>
Before jumping into tutorials, decide <strong>why</strong> you want to learn Python.
Your goal will define what you focus on:
</p>
<ul>
  <li><strong>Automation / IT support</strong> – scripts to automate boring tasks.</li>
  <li><strong>Web backend</strong> – APIs and web apps with Flask or Django.</li>
  <li><strong>Data / Analytics</strong> – work with CSV, Excel, SQL, dashboards.</li>
  <li><strong>Freelance projects</strong> – small tools or scripts for clients.</li>
</ul>
<p>
Pick <strong>one</strong> for the next 3–6 months. You can always switch later, but
starting with a clear direction will save you months of confusion.
</p>

<h2>Step 2: Learn the fundamentals (and finish one course)</h2>
<p>
Stop jumping from YouTube video to YouTube video. Instead:
</p>
<ol>
  <li>Choose <strong>one beginner-friendly course</strong> (free or paid).</li>
  <li>Commit to finishing it 100%.</li>
  <li>Write code <em>with</em> the instructor, don’t just watch.</li>
</ol>
<p>
Good options for beginners:
</p>
<ul>
  <li><strong>Python for Everybody</strong> (Coursera)</li>
  <li><strong>freeCodeCamp</strong> Python full course on YouTube</li>
  <li><strong>Automate the Boring Stuff with Python</strong> (book + videos)</li>
</ul>
<p>
The key is not which course you choose. The key is to <strong>finish it</strong>
and write code every week.
</p>

<h2>Step 3: Build 3–5 small, real projects</h2>
<p>
Tutorials teach you the basics. Projects teach you how to think.
Here are project ideas you can actually show in a CV or portfolio:
</p>
<ul>
  <li>A script that cleans and merges CSV files for a fake “sales team”.</li>
  <li>A small Flask app that lets users save notes or tasks.</li>
  <li>A script that renames and organizes files in a messy folder.</li>
  <li>A dashboard (with Streamlit) that reads an Excel and shows charts.</li>
</ul>
<p>
Keep each project <strong>simple, but finished</strong>. It’s better to have 3 small projects
that work than one “big system” that is always 80% done.
</p>

<h2>Step 4: Learn the basics of Git and GitHub</h2>
<p>
If you want a job or freelance work, people need to <strong>see</strong> your code.
That’s what GitHub is for.
</p>
<ul>
  <li>Create a GitHub account.</li>
  <li>Upload each project in a separate repository.</li>
  <li>Add a simple README explaining what the project does.</li>
</ul>
<p>
Even junior recruiters and clients will check your GitHub when you mention
Python on your resume.
</p>

<h2>Step 5: Add Python to your CV the right way</h2>
<p>
Don’t just write: “Python – intermediate”. That doesn’t mean anything.
Instead, be specific:
</p>
<ul>
  <li><strong>Python:</strong> scripts for automation and working with CSV/Excel files.</li>
  <li><strong>Flask:</strong> small web apps and APIs.</li>
  <li><strong>Tools:</strong> Git, GitHub, VS Code.</li>
</ul>
<p>
If you have no professional experience yet, you can use a section like
“Personal Projects” and list your 3–5 mini projects with 1–2 bullet points each.
</p>

<h2>Step 6: Start applying earlier than you think</h2>
<p>
Most people wait until they are “experts” to apply. Big mistake.
Once you have:
</p>
<ul>
  <li>basic Python fundamentals,</li>
  <li>3–5 small projects on GitHub,</li>
  <li>a CV that clearly shows your skills,</li>
</ul>
<p>
you can start applying to:
</p>
<ul>
  <li>Internships and trainee positions.</li>
  <li>Junior Python / backend / data roles.</li>
  <li>Simple freelance gigs (Upwork, Fiverr, local businesses).</li>
</ul>

<h2>Step 7: Keep improving while you apply</h2>
<p>
Getting your first opportunity can take months. The worst thing you can do
is stop learning while you wait.
</p>
<p>
A good weekly rhythm could be:
</p>
<ul>
  <li>3–4 days: study + build small features or fixes for your projects.</li>
  <li>2–3 days: send applications and improve your CV / LinkedIn.</li>
</ul>

<h2>Final advice</h2>
<p>
Your Python career in 2026 won’t depend on knowing every library.
It will depend on:
</p>
<ul>
  <li>Finishing what you start.</li>
  <li>Building small, real, visible projects.</li>
  <li>Showing your work to the right people.</li>
</ul>
<p>
If you stay consistent for 6–12 months, starting from zero,
you’ll be far ahead of most people who only “watch tutorials”.
</p>
"""

    cur.execute(
        """
        INSERT INTO posts (title, slug, date, tags, excerpt, content)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, slug, date_str, tags, excerpt, content_html.strip()),
    )

    conn.commit()
    conn.close()
    print("✔ Post insertado correctamente en la base de datos.")

if __name__ == "__main__":
    main()
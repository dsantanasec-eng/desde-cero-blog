from datetime import datetime
import sqlite3
from pathlib import Path

# Ruta a la base de datos (igual que en main.py)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # --------- DATOS DEL POST NUEVO (EN INGLÉS, PARA USA) ---------
    title = "7 Python projects for absolute beginners (that look great on your CV)"
    slug = "python-beginner-projects-usa-2026"  # debe ser ÚNICO en la tabla posts

    # fecha actual en formato 'YYYY-MM-DD HH:MM:SS'
    date_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    tags = "python, beginners, projects, portfolio, usa, english"

    excerpt = (
        "A practical list of beginner-friendly Python projects you can build to "
        "practice real skills and create a portfolio that attracts remote opportunities in the US."
    )

    content_html = """
<h2>Why beginner projects matter</h2>
<p>
If you want a Python job or freelance work in the US, you need more than theory.
Recruiters want to see <strong>real projects</strong> that prove you can solve
practical problems. The good news: you don't need anything advanced to start.
Simple projects, done well, are enough to stand out as a beginner.
</p>

<h2>7 Python projects for absolute beginners</h2>

<h3>1. Personal expense tracker (CLI or simple app)</h3>
<p>
Build a small program where you type your daily expenses and the script
stores them in a file or a simple database, then shows totals by day
or category. This teaches you how to work with input, files, and basic
data analysis – skills that are useful for any junior role.
</p>

<h3>2. Habit tracker with weekly report</h3>
<p>
Create a script where you log habits like <em>study Python</em>,
<em>go to the gym</em> or <em>read 15 minutes</em>. At the end of the week
the program prints a summary: how many days you completed each habit.
This project shows discipline and also gives you practice with dates,
loops and simple reports.
</p>

<h3>3. Password generator (with safety rules)</h3>
<p>
Write a tool that generates strong random passwords following rules:
minimum length, upper and lower case letters, digits and symbols.
You can also add an option to create several passwords at once.
This is a classic beginner project and looks good if you are
interested in IT support, cybersecurity or sysadmin roles.
</p>

<h3>4. Simple API-based weather checker</h3>
<p>
Use a free weather API to ask for the current weather in a city.
The user types the city name and your script prints temperature,
conditions and maybe a short suggestion like “take an umbrella”.
This is your first contact with real-world APIs, HTTP requests
and JSON – all very valuable in US tech jobs.
</p>

<h3>5. URL shortener (local version)</h3>
<p>
Create a small app where the user pastes a long URL and your script
creates a shorter code (for example, using a random string) and stores
the mapping in a file or SQLite. Later, when the user enters the short
code, your app returns the original link. This project teaches you about
mapping IDs to data and is a nice step toward web development.
</p>

<h3>6. Study planner for Python learning</h3>
<p>
Build a script where the user writes how many hours per week they can
study and in how many months they want to finish a beginner roadmap.
Your program suggests how many hours per day they should study and
prints a simple plan. This shows that you understand the learning
process and care about productivity, which is attractive for remote
US companies.
</p>

<h3>7. Simple blog content idea generator</h3>
<p>
Create a program that asks for a topic, for example “Python for data
analysis” or “IT support for beginners”, and then generates several
blog post ideas by combining templates you write manually. This is a
fun project that connects Python with content creation and marketing,
very useful if you want to attract traffic from the US to your own blog.
</p>

<h2>How to use these projects in your portfolio</h2>
<p>
You do not need to build all seven projects at once. Start with one,
finish it, and upload the code to GitHub. Add a short README explaining
what the project does, how to run it, and what you learned. When you
apply for jobs or freelance gigs in the US, you can link directly to
these projects so clients see that you can learn fast and deliver
something real, even as a beginner.
</p>
"""

    # --------- INSERTAR EN LA BASE DE DATOS ---------
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
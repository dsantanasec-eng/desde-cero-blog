import sqlite3
from pathlib import Path
from datetime import datetime

# Ruta a la base de datos
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    title = "7 Beginner Cybersecurity Projects That Actually Help You Get a Job"
    slug = "beginner-cybersecurity-projects-usa-2025"

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    tags = "cybersecurity, beginner, projects, usa, career, portfolio"

    excerpt = (
        "If you're starting in cybersecurity, projects matter more than certificates. "
        "These beginner-friendly projects help you build real skills, confidence, and a portfolio "
        "that recruiters in the U.S. actually care about."
    )

    content_html = """
    <h2>Why beginner cybersecurity projects matter</h2>
    <p>
    In the U.S. tech market, employers care less about theory and more about proof.
    Projects show that you can apply knowledge, solve problems, and think like a security professional.
    </p>

    <h2>1. Password Strength Checker</h2>
    <p>
    This project teaches you about authentication risks and brute-force attacks.
    It shows employers you understand basic security hygiene.
    </p>

    <h2>2. Simple Port Scanner (Python)</h2>
    <p>
    A classic beginner project that introduces networking fundamentals and how attackers discover open services.
    </p>

    <h2>3. Log Analyzer for Suspicious Activity</h2>
    <p>
    Teaches you how SOC analysts detect anomalies using real log data.
    </p>

    <h2>4. Phishing Email Detector</h2>
    <p>
    Extremely relevant in the U.S. job market where phishing is the #1 attack vector.
    </p>

    <h2>5. File Integrity Monitor</h2>
    <p>
    Shows understanding of malware detection and system monitoring.
    </p>

    <h2>6. Basic Vulnerability Scanner</h2>
    <p>
    Introduces you to CVEs, scanning logic, and risk assessment.
    </p>

    <h2>7. Simple Firewall Rules Simulator</h2>
    <p>
    Demonstrates knowledge of traffic filtering and network security concepts.
    </p>

    <h2>Final advice</h2>
    <p>
    You don't need expensive certifications to start.
    One solid project explained well can open doors faster than you think.
    </p>
    """

    cur.execute(
        """
        INSERT INTO posts (title, slug, date, tags, excerpt, content)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, slug, date_str, tags, excerpt, content_html.strip())
    )

    conn.commit()
    conn.close()

    print("✅ Post USA inserted successfully")

if __name__ == "__main__":
    main()
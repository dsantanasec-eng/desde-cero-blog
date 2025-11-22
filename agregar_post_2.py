import sqlite3
from pathlib import Path
from datetime import datetime

# Ruta al archivo de base de datos
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mi_blog.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# ====== DATOS DEL POST NUEVO ======
title = "5 razones por las que aprender Python en 2026 puede cambiar tu vida profesional"
slug = "5-razones-para-aprender-python-en-2026"
date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
tags = "python, carrera, tecnología, futuro"
excerpt = (
    "Un resumen claro y directo de por qué aprender Python en 2026 "
    "puede abrirte puertas en empleo, dinero y oportunidades reales."
)

content = """
<p>Python no es solo un lenguaje de programación. En 2026 se ha convertido en una
herramienta clave para quienes quieren crecer profesionalmente, ganar mejores salarios
y entrar a industrias que están explotando en demanda.</p>

<h2>1. Altísima demanda laboral</h2>
<p>Las empresas están buscando perfiles que dominen Python para desarrollo web,
automatización, análisis de datos y seguridad. Es uno de los lenguajes más pedidos
en ofertas remotas y presenciales.</p>

<h2>2. Ideal para comenzar desde cero</h2>
<p>Python tiene una sintaxis sencilla, parecida al inglés. No necesitas experiencia
previa para empezar. Miles de personas han conseguido su primer empleo tech usando Python.</p>

<h2>3. Sueldos competitivos</h2>
<p>Los roles asociados a Python —como backend developer, data analyst o automation engineer—
son de los mejores pagados en la industria tecnológica.</p>

<h2>4. Te abre puertas en muchas áreas</h2>
<ul>
  <li>Desarrollo web</li>
  <li>Ciberseguridad</li>
  <li>Inteligencia artificial y machine learning</li>
  <li>Automatización de tareas</li>
  <li>Análisis de datos</li>
</ul>

<h2>5. Comunidad gigante y recursos gratis</h2>
<p>La comunidad de Python es enorme. Hay cursos, tutoriales, foros y proyectos listos para usar.
Nunca estarás solo mientras aprendes.</p>

<h2>Conclusión</h2>
<p>Si estás buscando una habilidad real, con oportunidades reales y futuro asegurado,
Python es una apuesta inteligente en 2026.</p>

<p>Este blog te acompañará paso a paso para aprenderlo de forma práctica.</p>
"""

# ====== INSERTAR EN LA TABLA posts ======
cur.execute(
    """
    INSERT INTO posts (title, slug, date, tags, excerpt, content)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (title, slug, date, tags, excerpt, content.strip()),
)

conn.commit()
conn.close()

print("✔ Post insertado con slug:", slug)
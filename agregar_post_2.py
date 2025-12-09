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

    # ----------------------------
    # DATOS DEL NUEVO POST (ESTE ES NUEVO, NO EXISTE EN TU DB)
    # ----------------------------

    title = "Cómo obtener tu primer trabajo remoto en tecnología sin experiencia (Guía 2025)"
    slug = "primer-trabajo-remoto-tecnologia"   # << NUEVO SLUG ÚNICO
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    tags = "tecnologia, remoto, primer empleo, carrera"
    
    excerpt = (
        "Una guía práctica para conseguir tu primer trabajo remoto en tecnología "
        "aunque estés empezando desde cero."
    )

    content_html = """
    <h2>¿Quieres trabajar remoto sin experiencia? Sí se puede.</h2>

    <p>En 2025, la industria tecnológica ofrece miles de oportunidades para personas 
    que están empezando desde cero. No necesitas un título universitario ni ser experto: 
    necesitas estrategia, constancia y un buen portafolio.</p>

    <h3>1. Aprende habilidades que están en demanda</h3>
    <ul>
        <li>Desarrollo web (HTML, CSS, JavaScript)</li>
        <li>Python para automatización</li>
        <li>Soporte técnico / IT Help Desk</li>
        <li>Ciberseguridad inicial</li>
    </ul>

    <h3>2. Construye un portafolio pequeño pero sólido</h3>
    <p>Crea solo 3 a 5 proyectos. No más. Cada uno debe resolver un problema real.</p>

    <h3>3. Optimiza tu perfil de LinkedIn</h3>
    <p>LinkedIn es una máquina de oportunidades. Un perfil optimizado atrae reclutadores.</p>

    <h3>4. Aplica a trabajos remotos de nivel junior</h3>
    <p>Recomendación: envía 15–20 aplicaciones por semana. La consistencia gana.</p>

    <h3>Conclusión</h3>
    <p>Tu primer trabajo remoto no requiere suerte. Requiere estrategia.</p>
    <p>Si sigues esta guía, puedes conseguir tu oportunidad este mismo año.</p>
    """

    # ----------------------------
    # GUARDAR EN LA BASE DE DATOS
    # ----------------------------

    cur.execute(
        """
        INSERT INTO posts (title, slug, date, tags, excerpt, content_html)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, slug, date_str, tags, excerpt, content_html.strip())
    )

    conn.commit()
    conn.close()
    print("✔ NUEVO POST AGREGADO CORRECTAMENTE")

if __name__ == "__main__":
    main()
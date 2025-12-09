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

    # ========= DATOS DEL NUEVO POST =========
    title = "7 errores comunes al aprender Python desde cero (y cómo evitarlos)"
    slug = "errores-comunes-aprender-python-desde-cero"  # 👈 SLUG NUEVO
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tags = "python, principiantes, programación, errores comunes"

    excerpt = (
        "Un resumen claro de los errores más frecuentes cuando empiezas con Python "
        "y cómo evitarlos para avanzar más rápido sin rendirte."
    )

    content_html = """
<p>Aprender Python puede cambiar tu vida profesional, pero es normal cometer errores al inicio.
La buena noticia es que casi todos cometen <strong>los mismos errores</strong>. Si los conoces antes,
puedes avanzar más rápido y con menos frustración.</p>

<h2>1. Querer aprender “todo” antes de empezar</h2>
<p>Muchos principiantes pasan horas buscando el curso perfecto, el libro perfecto o el canal perfecto.
La verdad es que <strong>no existe el recurso perfecto</strong>. Lo importante es elegir uno bueno, terminarlo
y practicar con proyectos pequeños.</p>

<p><em>Qué hacer:</em> elige un solo curso o libro básico de Python, márcalo como tu “ruta principal”
y comprométete a terminarlo antes de saltar a otro.</p>

<h2>2. Memorizar código en lugar de practicar</h2>
<p>Copiar código sin entenderlo es uno de los errores más peligrosos.
No necesitas memorizar todo; necesitas <strong>entender la lógica</strong> y practicar escribiendo código tú mismo.</p>

<p><em>Qué hacer:</em> después de ver una lección, intenta resolver un ejercicio sin mirar la solución.
Si te bloqueas, revisa la teoría y vuelve a intentarlo.</p>

<h2>3. Saltar temas básicos como si no importaran</h2>
<p>Variables, tipos de datos, condicionales, bucles y funciones son la base de todo.
Si no dominas esto, cualquier tema más avanzado (APIs, web, automatización, etc.) te va a frustrar.</p>

<p><em>Qué hacer:</em> dedica tiempo a practicar ejercicios sencillos de cada tema.
Es normal repetir muchos ejercicios hasta sentirte cómodo.</p>

<h2>4. Querer usar demasiadas herramientas desde el día uno</h2>
<p>Algunos principiantes quieren aprender Python, Docker, Linux, Git, frameworks web
y análisis de datos al mismo tiempo. Eso solo crea estrés.</p>

<p><em>Qué hacer:</em> primero domina lo básico de Python. Luego elige un camino:
<strong>automatización, desarrollo web, data, ciberseguridad</strong>, etc., y avanza paso a paso.</p>

<h2>5. Compararse con otras personas en redes sociales</h2>
<p>En redes ves personas que dicen que en 3 meses ya son “senior”.
Eso puede hacerte sentir lento, pero la realidad es que cada persona tiene su ritmo
y muchas historias en internet no muestran todo el contexto.</p>

<p><em>Qué hacer:</em> compárate contigo mismo: ¿sabes hoy más que hace un mes?
Si la respuesta es sí, vas por buen camino.</p>

<h2>6. No pedir ayuda cuando te trabas</h2>
<p>Quedarte bloqueado horas en un error que podrías resolver en 10 minutos
preguntando es una pérdida de energía tremenda.</p>

<p><em>Qué hacer:</em> aprende a buscar errores en Google, en la documentación oficial,
y si hace falta, pregunta en comunidades de Python o a alguien con más experiencia.</p>

<h2>7. Rendirse justo cuando iba a empezar a funcionar</h2>
<p>Muchos abandonan cuando llegan a una parte que se siente “difícil”:
funciones, clases, errores raros, etc. Pero normalmente, justo después de ese punto
es cuando todo empieza a tener sentido.</p>

<p><em>Qué hacer:</em> acepta que habrá momentos incómodos.
Tómalos como señal de que estás creciendo, no como señal de que “no sirves para esto”.</p>

<h2>Conclusión</h2>
<p>Python no es solo para genios ni para personas con título universitario.
Si evitas estos errores y te mantienes constante, puedes construir proyectos reales,
mejorar tu perfil profesional y abrirte puertas en tecnología, paso a paso.</p>
    """

    # ========= INSERTAR EN LA TABLA =========
    cur.execute(
        """
        INSERT INTO posts (title, slug, date, tags, excerpt, content)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, slug, date_str, tags, excerpt, content_html.strip()),
    )

    conn.commit()
    print("✅ Post creado correctamente con ID:", cur.lastrowid)
    conn.close()


if __name__ == "__main__":
    main()
import sqlite3
from pathlib import Path
from datetime import date

# Ruta de tu base de datos (en la raíz del proyecto)
DB_PATH = Path(__file__).resolve().parent / "mi_blog.db"

def add_post(title: str, slug: str, tags: str, excerpt: str, content: str):
    if not DB_PATH.exists():
        raise FileNotFoundError(f"No encuentro la base de datos en: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Verifica que la tabla exista
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='posts'
    """)
    if cur.fetchone() is None:
        conn.close()
        raise RuntimeError("No existe la tabla 'posts'. Asegúrate de haber corrido init_db.")

    today = date.today().isoformat()  # YYYY-MM-DD

    cur.execute("""
        INSERT INTO posts (title, slug, date, tags, excerpt, content)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, slug, today, tags, excerpt, content))

    conn.commit()
    conn.close()
    print("✅ Post agregado a la base de datos:", title)

if __name__ == "_main_":
    title = "Por qué decidí aprender C++ y cómo ha sido el proceso hasta ahora"
    slug = "por-que-aprender-cpp-y-como-ha-sido-mi-proceso"
    tags = "c++,programacion,aprendizaje,desarrollo"
    excerpt = "Quería entender qué pasa por debajo del código. C++ me obligó a pensar distinto: memoria, rendimiento y fundamentos. Esto es lo que he aprendido hasta ahora."

    content = """Durante mucho tiempo pensé que aprender a programar era solo elegir un lenguaje “popular” y ya. Python, JavaScript, algo rápido, algo que diera resultados visibles. Y aunque eso no está mal, en un punto me di cuenta de que quería entender qué estaba pasando realmente por debajo. No solo escribir código que funcione, sino saber por qué funciona.

Ahí fue cuando apareció C++.

No fue una decisión impulsiva ni porque alguien me dijo que era “el mejor lenguaje”. De hecho, muchas personas me advirtieron que C++ es difícil, que tiene una curva de aprendizaje fuerte, que puede frustrar. Y precisamente por eso me llamó la atención.

El primer choque con C++
Aprender C++ no se siente cómodo al inicio. No es un lenguaje que te lleve de la mano. Desde el primer momento te obliga a pensar: cómo se guarda la información, cómo se usa la memoria, qué está pasando realmente cuando ejecutas una instrucción.

Al principio cometí errores simples. Errores que en otros lenguajes pasan desapercibidos, aquí no. Pero lejos de desmotivarme, eso me hizo entender algo importante: C++ te enseña a ser más cuidadoso. Cada línea importa.

Lo que C++ me hizo entender
Más allá del lenguaje en sí, C++ me ayudó a comprender conceptos que antes solo veía por encima:
- Cómo funciona la memoria
- Qué diferencia hay entre una variable, una referencia y un puntero
- Por qué el rendimiento importa
- Cómo piensa la computadora, no solo el programador

Eso cambia totalmente la forma en que ves la programación. Incluso cuando vuelves a otros lenguajes, piensas diferente.

No lo aprendí “rápido”, y eso está bien
No intenté correr. Aprender C++ no fue ver mil tutoriales en un día. Fue lento: leer, escribir código, equivocarme, volver a leer, volver a intentar. Y creo que eso es lo correcto.

Lo recomiendo?
Sí, pero con honestidad. No es el primer lenguaje ideal si lo que buscas es resultados inmediatos o aplicaciones rápidas. Pero si quieres formarte como desarrollador, entender los fundamentos y fortalecer tu lógica, C++ aporta muchísimo.

Mi conclusión personal
Aprender C++ fue una decisión consciente. No fácil, no rápida, pero muy valiosa. Me obligó a pensar más, a respetar los detalles y a entender la programación desde adentro.

Todavía sigo aprendiendo. Todavía me equivoco. Pero ahora sé que cada línea de código que escribo tiene un propósito más claro. Y eso, para mí, ya valió la pena.
"""

    add_post(title, slug, tags, excerpt, content)
import os
import re

from google import genai
from google.genai import types
from pypdf import PdfReader



# -------------------------------------------------------------------------
# CARGA DE CONTEXTO DESDE EL DATASET LOCAL
# -------------------------------------------------------------------------
def cargar_contexto_dataset():
    contexto = ""

    rutas_candidatas = [
        os.path.join(os.path.dirname(__file__), "..", "dataset_rx"),
        os.path.abspath("dataset_rx"),
        os.path.abspath(os.path.join("data", "dataset_rx")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset_rx"))
    ]

    dir_valido = None

    for r in rutas_candidatas:
        if os.path.exists(r):
            dir_valido = r
            break

    if dir_valido:
        for archivo in sorted(os.listdir(dir_valido)):
            if archivo.endswith(".txt"):
                path = os.path.join(dir_valido, archivo)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        contenido = f.read().strip()

                    if contenido:
                        contexto += (
                            f"\n=== Contenido de {archivo} ===\n"
                            f"{contenido}\n"
                        )

                except Exception as e:
                    print(f"Error leyendo {archivo}: {e}")

    return contexto


# -------------------------------------------------------------------------
# CARGA DE LIBROS
# Los PDF se leen UNA SOLA VEZ y quedan guardados en memoria.
# -------------------------------------------------------------------------
libros_cache = {}


def cargar_libros():

    # Si ya fueron cargados, NO volver a leer los PDF
    if libros_cache:
        return libros_cache

    rutas_candidatas = [
        os.path.join(os.path.dirname(__file__), "..", "libros_rx"),
        os.path.abspath("libros_rx"),
        os.path.abspath(os.path.join("data", "libros_rx"))
    ]

    dir_valido = None

    for r in rutas_candidatas:
        if os.path.exists(r):
            dir_valido = r
            break

    if not dir_valido:
        print("⚠️ No se encontró la carpeta libros_rx.")
        return libros_cache

    print("📚 Primera carga de los libros...")

    for archivo in sorted(os.listdir(dir_valido)):

        if not archivo.lower().endswith(".pdf"):
            continue

        path = os.path.join(dir_valido, archivo)

        try:

            print(f"📖 Procesando: {archivo}")

            reader = PdfReader(path)

            paginas = []

            for numero, pagina in enumerate(reader.pages):

                try:
                    texto = pagina.extract_text()

                    if texto:
                        paginas.append(
                            f"\n[PÁGINA {numero + 1}]\n{texto}"
                        )

                except Exception as e:
                    print(
                        f"Error leyendo página "
                        f"{numero + 1} de {archivo}: {e}"
                    )

            libros_cache[archivo] = "\n".join(paginas)

            print(
                f"✅ {archivo} cargado: "
                f"{len(reader.pages)} páginas."
            )

        except Exception as e:
            print(f"❌ Error leyendo {archivo}: {e}")

    print("✅ Libros cargados en memoria.")

    return libros_cache


# -------------------------------------------------------------------------
# DETECTAR SI EL USUARIO REALMENTE PIDIÓ USAR LOS LIBROS
# -------------------------------------------------------------------------
def necesita_libros(pregunta):

    pregunta = pregunta.lower().strip()

    frases_libros = [
        "según los libros",
        "segun los libros",
        "según el libro",
        "segun el libro",
        "según bushong",
        "segun bushong",
        "según fauber",
        "segun fauber",
        "del libro",
        "de los libros",
        "en el libro",
        "en los libros",
        "libro de bushong",
        "libro de fauber"
    ]

    for frase in frases_libros:

        if frase in pregunta:
            return True

    return False


# -------------------------------------------------------------------------
# BUSCAR INFORMACIÓN RELEVANTE EN LOS LIBROS
# -------------------------------------------------------------------------
def buscar_en_libros(pregunta_usuario, max_fragmentos=5):

    libros = cargar_libros()

    if not libros:
        return ""

    palabras = re.findall(
        r"[a-záéíóúñü]{4,}",
        pregunta_usuario.lower()
    )

    palabras_importantes = [
        p for p in palabras
        if p not in {
            "como",
            "cómo",
            "funciona",
            "funcionan",
            "según",
            "segun",
            "libros",
            "libro",
            "explica",
            "explicame",
            "explícame",
            "sobre",
            "cual",
            "cuál",
            "que",
            "qué",
            "para",
            "entre",
            "desde",
            "donde",
            "dónde"
        }
    ]

    resultados = []

    for nombre_libro, texto in libros.items():

        paginas = re.split(
            r"\[PÁGINA \d+\]",
            texto
        )

        paginas_relevantes = []

        for numero, pagina in enumerate(paginas):

            pagina_limpia = pagina.strip()

            if not pagina_limpia:
                continue

            texto_minuscula = pagina_limpia.lower()

            coincidencias = 0

            for palabra in palabras_importantes:

                if palabra in texto_minuscula:
                    coincidencias += 1

            if coincidencias > 0:

                paginas_relevantes.append(
                    (
                        coincidencias,
                        numero,
                        pagina_limpia
                    )
                )

        paginas_relevantes.sort(
            key=lambda x: x[0],
            reverse=True
        )

        for coincidencias, numero, pagina in paginas_relevantes[:max_fragmentos]:

            resultados.append(
                (
                    coincidencias,
                    nombre_libro,
                    numero,
                    pagina
                )
            )

    resultados.sort(
        key=lambda x: x[0],
        reverse=True
    )

    resultados = resultados[:max_fragmentos]

    contexto_libros = ""

    for coincidencias, nombre_libro, numero, pagina in resultados:

        contexto_libros += (
            f"\n=== {nombre_libro} | Fragmento relacionado ===\n"
            f"{pagina}\n"
        )

    return contexto_libros


# -------------------------------------------------------------------------
# CACHÉ DE RESPUESTAS
# -------------------------------------------------------------------------
respuesta_cache = {}


def consultar_con_cache(prompt: str):

    prompt_limpio = prompt.strip().lower()

    if prompt_limpio in respuesta_cache:
        return respuesta_cache[prompt_limpio]

    return None


def guardar_en_cache(prompt: str, respuesta: str):

    prompt_limpio = prompt.strip().lower()

    if len(respuesta_cache) > 100:
        respuesta_cache.popitem()

    respuesta_cache[prompt_limpio] = respuesta


# -------------------------------------------------------------------------
# GENERAR RESPUESTA
# -------------------------------------------------------------------------
def generar_respuesta_rapida(pregunta_usuario: str):

    # -------------------------------------------------------------
    # REVISAR SI YA EXISTE UNA RESPUESTA
    # -------------------------------------------------------------
    respuesta_cached = consultar_con_cache(
        pregunta_usuario
    )

    if respuesta_cached:
        return respuesta_cached

    # -------------------------------------------------------------
    # DATASET LOCAL
    # Siempre se utiliza porque es pequeño.
    # -------------------------------------------------------------
    contexto_dataset = cargar_contexto_dataset()

    # -------------------------------------------------------------
    # LIBROS
    #
    # SOLO se buscan si el usuario pidió explícitamente
    # información de los libros.
    # -------------------------------------------------------------
    contexto_libros = ""

    usar_libros = necesita_libros(
        pregunta_usuario
    )

    if usar_libros:

        print("📚 El usuario pidió información de los libros.")

        contexto_libros = buscar_en_libros(
            pregunta_usuario,
            max_fragmentos=5
        )

    else:

        print("⚡ Pregunta normal: no se revisarán los PDF.")

    # -------------------------------------------------------------
    # PROMPT
    # -------------------------------------------------------------
    prompt_completo = f"""
Eres un asistente académico especializado en Imagenología y Rayos X.

Responde a la pregunta del usuario utilizando la información
de la base de conocimiento proporcionada.

Si existen fragmentos de libros debajo, utilízalos también
como referencia.

REGLAS:
- Responde de forma directa, clara y fácil de entender.
- Da primero la respuesta principal en 1 o 2 frases.
- Desarrolla solo la información necesaria.
- Evita explicaciones demasiado largas.
- No repitas información.
- Usa listas cortas cuando ayuden.
- Si preguntan por tipos o clasificación, menciona los tipos
  y explica brevemente cada uno.
- No incluyas detalles técnicos, fórmulas o materiales específicos
  a menos que sean necesarios.
- Mantén normalmente la respuesta entre 3 y 8 frases.
- Si la pregunta necesita más explicación para ser completa,
  puedes extenderte un poco.
- No cortes una idea ni una oración a la mitad.
- Termina siempre la respuesta correctamente.
- No inventes información que no esté respaldada por las fuentes.

BASE DE CONOCIMIENTO ACADÉMICA:
{contexto_dataset}

FRAGMENTOS RELEVANTES DE LOS LIBROS:
{contexto_libros}

PREGUNTA DEL USUARIO:
{pregunta_usuario}
"""

    api_key_actual = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key_actual:

        return (
            "Error: no se encontró GEMINI_API_KEY."
        )

    client = genai.Client(
        api_key=api_key_actual
    )

    try:

        # ---------------------------------------------------------
        # GEMINI
        # ---------------------------------------------------------
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt_completo,
            config=types.GenerateContentConfig(
                temperature=0.2
            )
        )

        respuesta_completa = response.text

        # ---------------------------------------------------------
        # GUARDAR RESPUESTA EN CACHÉ
        # ---------------------------------------------------------
        if respuesta_completa:

            guardar_en_cache(
                pregunta_usuario,
                respuesta_completa
            )

        return respuesta_completa

    except Exception as e:

        error_str = str(e)

        if (
            "429" in error_str
            or "RESOURCE_EXHAUSTED" in error_str
        ):

            return (
                "⚠️ Límite de consultas alcanzado temporalmente. "
                "Espera unos segundos e intenta de nuevo."
            )

        elif (
            "503" in error_str
            or "UNAVAILABLE" in error_str
        ):

            return (
                "⚠️ El servicio de la IA está experimentando "
                "alta demanda. Intenta de nuevo en un momento."
            )

        else:

            return (
                f"Error al conectar con la IA: {error_str}"
            )

# ============================================================
# COMPONENTE VISUAL DEL ASISTENTE GEMINI
# ============================================================

from dash import html, dcc


def mostrar_gemini():

    return html.Div(
        [

            html.H3(
                "🤖 Asistente Gemini RX"
            ),


            dcc.Textarea(
                id="input-pregunta-gemini",
                placeholder=(
                    "Escribe una pregunta sobre Rayos X, "
                    "imagenología o procesamiento..."
                ),
                style={
                    "width": "100%",
                    "height": 90
                }
            ),


            html.Button(
                "Consultar IA",
                id="btn-consultar-gemini",
                n_clicks=0
            ),


            dcc.Store(
                id="historial-gemini",
                data=[]
            ),


            html.Div(
                id="historial-visible-gemini",
                style={
                    "marginTop": "15px",
                    "whiteSpace": "pre-wrap"
                }
            )

        ]
    )
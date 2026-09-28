import os
import base64
import json
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "No se encontró GEMINI_API_KEY en el archivo .env."
    )

client = genai.Client(api_key=API_KEY)


# ============================================================
# PALABRAS RELACIONADAS CON RAYOS X
# ============================================================

PALABRAS_RX = [
    "rayos x",
    "rayos-x",
    "radiografía",
    "radiografia",
    "radiología",
    "radiologia",
    "imagenología",
    "imagenologia",
    "radiación",
    "radiacion",
    "detector",
    "detectores",
    "x-ray",
    "xray",
    "tomografía",
    "tomografia",
    "mamografía",
    "mamografia",
    "radiografía digital",
    "radiografia digital",
    "radiografía computarizada",
    "radiografia computarizada",
    "equipo de rayos x",
    "tubo de rayos x",
    "cr",
    "dr",
    "film screen",
    "película radiográfica",
    "pelicula radiografica",
        "formación de imagen",
    "formacion de imagen",
    "formación de la imagen",
    "formacion de la imagen",
    "imagen radiográfica",
    "imagen radiografica",
    "proceso de formación",
    "proceso de formacion",
    "adquisición de imagen",
    "adquisicion de imagen",
    "generación de imagen",
    "generacion de imagen",
    "receptor de imagen",
    "sistema de imagen"
]


# ============================================================
# COMPROBAR TEMA
# ============================================================

def es_tema_rx(texto):

    if not texto:
        return False

    texto = texto.lower()

    for palabra in PALABRAS_RX:

        if palabra in texto:
            return True

    return False


# ============================================================
# OBTENER CONTEXTO
# ============================================================

def obtener_contexto(historial):

    if not historial:
        return ""

    ultimos = historial[-5:]

    contexto = ""

    for mensaje in ultimos:

        pregunta = mensaje.get("pregunta", "")
        respuesta = mensaje.get("respuesta", "")

        if not isinstance(respuesta, str):
            respuesta = ""

        contexto += f"""
Usuario: {pregunta}
Asistente: {respuesta}
"""

    return contexto


# ============================================================
# DETECTAR TIPO DE VISUAL
# ============================================================

def detectar_tipo_visual(pregunta):

    texto = pregunta.lower()

    if (
        "cuadro comparativo" in texto
        or "tabla comparativa" in texto
        or "comparación" in texto
        or "comparacion" in texto
        or "comparar" in texto
    ):
        return "comparacion"

    if (
        "mapa conceptual" in texto
        or "mapa mental" in texto
        or "mapa de conceptos" in texto
    ):
        return "mapa"

    if (
        "diagrama" in texto
        or "esquema" in texto
        or "proceso" in texto
        or "funcionamiento" in texto
    ):
        return "diagrama"

    return "diagrama"


# ============================================================
# PEDIR INFORMACIÓN ESTRUCTURADA A GEMINI
# ============================================================

def obtener_datos_gemini(
    pregunta,
    contexto,
    tipo_visual
):


    # ====================================================
    # PLANTILLA CR VS DR (SIN CONSUMIR GEMINI)
    # ====================================================

    if (
        "cr" in pregunta.lower()
        and "dr" in pregunta.lower()
    ):

        return {
            "titulo": "Comparación entre CR y DR",

            "columnas": [
                "CR",
                "DR"
            ],

            "filas": [
                {
                    "caracteristica": "Tecnología del detector",
                    "valores": [
                        "Placa de fósforo fotoestimulable",
                        "Detector digital"
                    ]
                },

                {
                    "caracteristica": "Procesamiento",
                    "valores": [
                        "Requiere lector CR",
                        "Procesamiento inmediato"
                    ]
                },

                {
                    "caracteristica": "Velocidad de adquisición",
                    "valores": [
                        "Más lento",
                        "Más rápido"
                    ]
                },

                {
                    "caracteristica": "Conversión de imagen",
                    "valores": [
                        "Escaneo de placa",
                        "Conversión directa"
                    ]
                }
            ]
        }

    if tipo_visual == "comparacion":

        instrucciones = """
Crea la información para un CUADRO COMPARATIVO.

Debes identificar los conceptos que el usuario quiere comparar
y seleccionar únicamente las características más importantes.

No escribas explicaciones largas.
"""

    elif tipo_visual == "mapa":

        instrucciones = """
Crea la información para un MAPA CONCEPTUAL.

Identifica el concepto principal y sus conceptos relacionados.
Organiza la información desde lo general hacia lo específico.

No escribas explicaciones largas.
"""

    else:

        instrucciones = """
Crea la información para un DIAGRAMA EDUCATIVO.

Identifica los componentes principales y la relación o secuencia
entre ellos.

No escribas explicaciones largas.
"""


    prompt = f"""
Eres un asistente académico especializado exclusivamente
en Rayos X e Imagenología.

Solicitud del usuario:
{pregunta}

Contexto anterior:
{contexto}

{instrucciones}

Devuelve ÚNICAMENTE un objeto JSON válido.

Tipo de visual:
{tipo_visual}

Si es una comparación usa exactamente esta estructura:

{{
    "titulo": "título",
    "columnas": ["Concepto A", "Concepto B"],
    "filas": [
        {{
            "caracteristica": "Característica",
            "valores": ["Dato A", "Dato B"]
        }}
    ]
}}

Si es un mapa conceptual usa:

{{
    "titulo": "Concepto principal",
    "conceptos": [
        "Concepto 1",
        "Concepto 2",
        "Concepto 3"
    ],
    "relaciones": [
        {{
            "origen": "Concepto principal",
            "destino": "Concepto 1"
        }}
    ]
}}

Si es un diagrama usa:

{{
    "titulo": "Título",
    "pasos": [
        "Paso 1",
        "Paso 2",
        "Paso 3"
    ]
}}

REGLAS:

- Información correcta de Rayos X.
- Solo información necesaria.
- No inventes conceptos.
- No uses Markdown.
- No uses ```json.
- Devuelve solamente JSON.
"""

    respuesta = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2
        )
    )

    texto = respuesta.text.strip()

    # --------------------------------------------------------
    # Limpiar posibles bloques de código
    # --------------------------------------------------------

    if texto.startswith("```"):

        texto = texto.replace("```json", "")
        texto = texto.replace("```", "")
        texto = texto.strip()

    return json.loads(texto)


# ============================================================
# CREAR CUADRO COMPARATIVO
# ============================================================

def crear_comparacion(datos):

    titulo = datos.get(
        "titulo",
        "Comparación"
    )

    columnas = datos.get(
        "columnas",
        []
    )

    filas = datos.get(
        "filas",
        []
    )

    if len(columnas) < 2:
        raise ValueError(
            "No se recibieron suficientes columnas."
        )

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    ax.axis("off")

    encabezados = [
        "Característica"
    ] + columnas

    contenido = []

    for fila in filas:

        contenido.append(
            [
                fila.get("caracteristica", ""),
                *fila.get("valores", [])
            ]
        )

    tabla = ax.table(
        cellText=contenido,
        colLabels=encabezados,
        cellLoc="center",
        loc="center"
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1, 2)

    ax.set_title(
        titulo,
        fontsize=18,
        fontweight="bold",
        pad=20
    )

    plt.tight_layout()

    return figura_a_base64(fig)


# ============================================================
# CREAR MAPA CONCEPTUAL
# ============================================================

def crear_mapa(datos):

    titulo = datos.get(
        "titulo",
        "Mapa conceptual"
    )

    conceptos = datos.get(
        "conceptos",
        []
    )

    relaciones = datos.get(
        "relaciones",
        []
    )

    fig, ax = plt.subplots(
        figsize=(12, 8)
    )

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # --------------------------------------------------------
    # Posición del concepto principal
    # --------------------------------------------------------

    posiciones = {}

    posiciones[titulo] = (6, 8)

    # --------------------------------------------------------
    # Posiciones de conceptos secundarios
    # --------------------------------------------------------

    cantidad = len(conceptos)

    if cantidad > 0:

        separacion = 10 / max(cantidad, 1)

        for i, concepto in enumerate(conceptos):

            x = 1 + (i * separacion)

            posiciones[concepto] = (
                x,
                4.5
            )

    # --------------------------------------------------------
    # Dibujar relaciones
    # --------------------------------------------------------

    for relacion in relaciones:

        origen = relacion.get(
            "origen",
            ""
        )

        destino = relacion.get(
            "destino",
            ""
        )

        if (
            origen in posiciones
            and destino in posiciones
        ):

            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]

            flecha = FancyArrowPatch(
                (x1, y1 - 0.5),
                (x2, y2 + 0.5),
                arrowstyle="->",
                mutation_scale=15
            )

            ax.add_patch(flecha)

    # --------------------------------------------------------
    # Dibujar cajas
    # --------------------------------------------------------

    for concepto, (x, y) in posiciones.items():

        if concepto == titulo:

            ancho = 3.2
            alto = 1.0

        else:

            ancho = 2.2
            alto = 0.9

        caja = FancyBboxPatch(
            (
                x - ancho / 2,
                y - alto / 2
            ),
            ancho,
            alto,
            boxstyle="round,pad=0.05"
        )

        ax.add_patch(caja)

        ax.text(
            x,
            y,
            concepto,
            ha="center",
            va="center",
            fontsize=10,
            wrap=True
        )

    ax.set_title(
        "Mapa conceptual",
        fontsize=18,
        fontweight="bold"
    )

    plt.tight_layout()

    return figura_a_base64(fig)


# ============================================================
# CREAR DIAGRAMA
# ============================================================

def crear_diagrama(datos):

    titulo = datos.get(
        "titulo",
        "Diagrama"
    )

    pasos = datos.get(
        "pasos",
        []
    )

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis("off")

    cantidad = len(pasos)

    if cantidad == 0:
        raise ValueError(
            "No se recibieron pasos para el diagrama."
        )

    espacio = 8 / cantidad

    posiciones = []

    for i, paso in enumerate(pasos):

        x = 2 + i * espacio
        y = 5

        posiciones.append(
            (x, y)
        )

        caja = FancyBboxPatch(
            (
                x - 1.2,
                y - 0.6
            ),
            2.4,
            1.2,
            boxstyle="round,pad=0.05"
        )

        ax.add_patch(caja)

        ax.text(
            x,
            y,
            paso,
            ha="center",
            va="center",
            fontsize=10,
            wrap=True
        )

    # --------------------------------------------------------
    # Flechas
    # --------------------------------------------------------

    for i in range(
        len(posiciones) - 1
    ):

        x1, y1 = posiciones[i]
        x2, y2 = posiciones[i + 1]

        flecha = FancyArrowPatch(
            (
                x1 + 1.2,
                y1
            ),
            (
                x2 - 1.2,
                y2
            ),
            arrowstyle="->",
            mutation_scale=15
        )

        ax.add_patch(flecha)

    ax.set_title(
        titulo,
        fontsize=18,
        fontweight="bold"
    )

    plt.tight_layout()

    return figura_a_base64(fig)


# ============================================================
# CONVERTIR FIGURA A BASE64
# ============================================================

def figura_a_base64(fig):

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    buffer.seek(0)

    imagen_bytes = buffer.getvalue()

    return base64.b64encode(
        imagen_bytes
    ).decode("utf-8")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def generar_visual_rx(
    pregunta,
    historial=None
):

    if historial is None:
        historial = []

    # --------------------------------------------------------
    # Comprobar tema
    # --------------------------------------------------------

    contexto = obtener_contexto(
        historial
    )

    texto_completo = f"""
{pregunta}

{contexto}
"""

    if not es_tema_rx(
        texto_completo
    ):

        return {
            "ok": False,
            "error": (
                "Solo puedo generar visuales relacionados "
                "con Rayos X e Imagenología."
            )
        }

    try:

        # ----------------------------------------------------
        # Detectar tipo
        # ----------------------------------------------------

        tipo_visual = detectar_tipo_visual(
            pregunta
        )

        # ----------------------------------------------------
        # Obtener información de Gemini
        # ----------------------------------------------------

        datos = obtener_datos_gemini(
            pregunta,
            contexto,
            tipo_visual
        )

        # ----------------------------------------------------
        # Crear visual
        # ----------------------------------------------------

        if tipo_visual == "comparacion":

            imagen = crear_comparacion(
                datos
            )

        elif tipo_visual == "mapa":

            imagen = crear_mapa(
                datos
            )

        else:

            imagen = crear_diagrama(
                datos
            )

        return {
            "ok": True,
            "imagen": imagen,
            "mime_type": "image/png"
        }

    except Exception as e:

        return {
            "ok": False,
            "error": (
                f"Error al crear el visual: {str(e)}"
            )
        }
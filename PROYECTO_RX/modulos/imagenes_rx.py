import os
import base64
import re
from io import BytesIO

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# ============================================================
# PALABRAS RELACIONADAS CON RAYOS X
# ============================================================

PALABRAS_RX = [
    "rayos x",
    "rayos-x",
    "rayosx",
    "radiografía",
    "radiografia",
    "radiográfico",
    "radiografico",
    "radiología",
    "radiologia",
    "radiológico",
    "radiologico",
    "radiografía médica",
    "equipo de rayos x",
    "máquina de rayos x",
    "maquina de rayos x",
    "imagen médica",
    "imagen medica",
    "detector",
    "detectores",
    "cr",
    "dr",
    "ccd",
    "cmos",
    "tft",
    "tubo de rayos x",
    "tubo de rayos-x",
    "sala de radiología",
    "sala de radiologia",
]


# ============================================================
# COMPROBAR SI EL TEMA ES DE RAYOS X
# ============================================================

def es_tema_rx(texto):
    texto = texto.lower()

    # Palabras de varias palabras
    for palabra in PALABRAS_RX:
        if " " in palabra or "-" in palabra:
            if palabra in texto:
                return True

    # Palabras individuales
    palabras_individuales = [
        "radiografía",
        "radiografia",
        "radiología",
        "radiologia",
        "detector",
        "detectores",
        "ccd",
        "cmos",
        "tft",
    ]

    for palabra in palabras_individuales:
        if re.search(r"\b" + re.escape(palabra) + r"\b", texto):
            return True

    # CR y DR necesitan comprobación especial porque son siglas
    if re.search(r"\bcr\b", texto):
        return True

    if re.search(r"\bdr\b", texto):
        return True

    return False


# ============================================================
# CONTEXTO DEL HISTORIAL
# ============================================================

def obtener_contexto(historial):
    if not historial:
        return ""

    ultimos = historial[-6:]

    contexto = []

    for mensaje in ultimos:
        if isinstance(mensaje, dict):
            pregunta = mensaje.get("pregunta", "")
            respuesta = mensaje.get("respuesta", "")

            if pregunta:
                contexto.append(f"Pregunta: {pregunta}")

            if respuesta:
                contexto.append(f"Respuesta: {respuesta}")

    return "\n".join(contexto)


# ============================================================
# DETECTAR TIPO DE IMAGEN
# ============================================================

def detectar_tipo_imagen(pregunta):
    """
    Detecta automáticamente qué tipo de imagen
    está solicitando el estudiante.
    """

    texto = pregunta.lower().strip()

    # --------------------------------------------------------
    # 1. RADIOGRAFÍA
    # --------------------------------------------------------

    palabras_radiografia = [
        "radiografía",
        "radiografia",
        "placa",
        "imagen radiográfica",
        "imagen radiografica",
        "radiografía de tórax",
        "radiografia de torax",
        "radiografía de pecho",
        "radiografia de pecho",
        "rayos x de tórax",
        "rayos x de torax",
    ]

    for palabra in palabras_radiografia:
        if palabra in texto:
            if "tórax" in texto or "torax" in texto or "pecho" in texto:
                return "radiografia_torax"

            return "radiografia"


    # --------------------------------------------------------
    # 2. EQUIPO DE RAYOS X
    # --------------------------------------------------------

    palabras_equipo = [
        "equipo de rayos x",
        "equipo de rayos-x",
        "máquina de rayos x",
        "maquina de rayos x",
        "máquina de rayos-x",
        "maquina de rayos-x",
        "aparato de rayos x",
        "aparato de rayos-x",
        "sistema de rayos x",
        "sistema radiográfico",
        "sistema radiografico",
        "equipo radiográfico",
        "equipo radiografico",
    ]

    for palabra in palabras_equipo:
        if palabra in texto:
            return "equipo_rayos_x"


    # --------------------------------------------------------
    # 3. TUBO DE RAYOS X
    # --------------------------------------------------------

    palabras_tubo = [
        "tubo de rayos x",
        "tubo de rayos-x",
        "tubo radiográfico",
        "tubo radiografico",
        "tubo de rayos",
        "ánodo",
        "anodo",
        "cátodo",
        "catodo",
    ]

    for palabra in palabras_tubo:
        if palabra in texto:
            return "tubo_rayos_x"


    # --------------------------------------------------------
    # 4. DETECTOR
    # --------------------------------------------------------

    palabras_detector = [
        "detector",
        "detectores",
        "detector de rayos x",
        "detector de rayos-x",
        "detector dr",
        "detector cr",
        "detector digital",
        "panel detector",
        "panel plano",
        "flat panel",
        "receptor de imagen",
    ]

    for palabra in palabras_detector:
        if palabra in texto:
            return "detector"


    # --------------------------------------------------------
    # 5. CR
    # --------------------------------------------------------

    if re.search(r"\bcr\b", texto):
        return "detector_cr"

    if "computed radiography" in texto:
        return "detector_cr"

    if "radiografía computarizada" in texto:
        return "detector_cr"

    if "radiografia computarizada" in texto:
        return "detector_cr"


    # --------------------------------------------------------
    # 6. DR
    # --------------------------------------------------------

    if re.search(r"\bdr\b", texto):
        return "detector_dr"

    if "digital radiography" in texto:
        return "detector_dr"

    if "radiografía digital" in texto:
        return "detector_dr"

    if "radiografia digital" in texto:
        return "detector_dr"


    # --------------------------------------------------------
    # 7. CONSOLA / PANEL DE CONTROL
    # --------------------------------------------------------

    palabras_consola = [
        "consola",
        "panel de control",
        "control de rayos x",
        "panel de mando",
        "estación de trabajo",
        "estacion de trabajo",
        "computadora de rayos x",
    ]

    for palabra in palabras_consola:
        if palabra in texto:
            return "consola"


    # --------------------------------------------------------
    # 8. SALA DE RADIOLOGÍA
    # --------------------------------------------------------

    palabras_sala = [
        "sala de radiología",
        "sala de radiologia",
        "sala radiográfica",
        "sala radiografica",
        "habitación de rayos x",
        "habitacion de rayos x",
        "cuarto de rayos x",
        "sala de rayos x",
    ]

    for palabra in palabras_sala:
        if palabra in texto:
            return "sala_radiologia"


    # --------------------------------------------------------
    # 9. PARTES DEL EQUIPO
    # --------------------------------------------------------

    palabras_partes = [
        "partes del equipo",
        "componentes del equipo",
        "partes de la máquina",
        "partes de la maquina",
        "componentes de rayos x",
        "componentes del sistema",
    ]

    for palabra in palabras_partes:
        if palabra in texto:
            return "partes_equipo"


    # --------------------------------------------------------
    # 10. IMAGEN GENERAL
    # --------------------------------------------------------

    return "general"


# ============================================================
# CREAR PROMPT SEGÚN EL TIPO
# ============================================================

def crear_prompt_imagen(pregunta, tipo, contexto=""):

    prompts = {

        # ----------------------------------------------------
        # EQUIPO COMPLETO
        # ----------------------------------------------------

        "equipo_rayos_x": """
Create a realistic high-quality photograph of a modern medical
X-ray radiography machine inside a hospital radiology room.

Show the COMPLETE X-ray equipment clearly, including:
- X-ray tube housing
- support arm
- radiographic table
- image detector
- structural components of the machine

The equipment must be clearly recognizable as a real medical
radiography system.

Professional medical photography.
Realistic materials and proportions.
Sharp focus.
High resolution.
Clean modern hospital environment.

DO NOT show an X-ray radiograph.
DO NOT show human anatomy.
DO NOT create a diagram.
DO NOT add labels.
DO NOT add text.
DO NOT add letters.
DO NOT add arrows.
DO NOT add captions.
DO NOT add symbols.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # TUBO
        # ----------------------------------------------------

        "tubo_rayos_x": """
Create a realistic detailed medical photograph of an X-ray tube
used in diagnostic radiography.

Clearly show the X-ray tube housing and its main physical structure.
Show realistic medical engineering details and materials.

Professional university medical reference image.
Sharp focus.
High resolution.
Clean neutral background.

DO NOT add labels.
DO NOT add text.
DO NOT add letters.
DO NOT add arrows.
DO NOT create a diagram.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # DETECTOR GENERAL
        # ----------------------------------------------------

        "detector": """
Create a realistic high-quality medical photograph of a modern
digital X-ray detector.

Show a flat-panel X-ray detector used in diagnostic radiography.
The detector should be clearly visible as a real medical device,
with realistic dimensions, casing, surface and construction.

Professional medical equipment photography.
Sharp focus.
High detail.
Clean neutral background.

DO NOT add labels.
DO NOT add text.
DO NOT add letters.
DO NOT add arrows.
DO NOT create a diagram.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # DETECTOR CR
        # ----------------------------------------------------

        "detector_cr": """
Create a realistic medical photograph of a Computed Radiography
(CR) imaging plate and CR reader used in X-ray imaging.

Clearly show the imaging plate and the CR reader as real medical
equipment used in a radiology department.

Professional medical equipment photography.
Sharp focus.
High detail.
Realistic materials.

DO NOT add labels.
DO NOT add text.
DO NOT add letters.
DO NOT add arrows.
DO NOT create a comparison table.
DO NOT create a diagram.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # DETECTOR DR
        # ----------------------------------------------------

        "detector_dr": """
Create a realistic medical photograph of a Digital Radiography
(DR) flat-panel detector.

Show a modern flat-panel digital X-ray detector as a real medical
device used in a radiology department.

Professional medical equipment photography.
Sharp focus.
High detail.
Realistic proportions and materials.

DO NOT add labels.
DO NOT add text.
DO NOT add letters.
DO NOT add arrows.
DO NOT create a comparison table.
DO NOT create a diagram.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # RADIOGRAFÍA GENERAL
        # ----------------------------------------------------

        "radiografia": """
Create a realistic diagnostic medical X-ray radiograph.

Show a genuine-looking radiographic image with realistic
X-ray grayscale appearance, anatomical structures and
medical imaging characteristics.

The result should look like a clinical radiographic image
used for university radiology education.

Sharp anatomical structures.
Good contrast.
High resolution.

DO NOT add explanatory text.
DO NOT add labels.
DO NOT add arrows.
DO NOT add diagrams.
DO NOT add random objects.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # RADIOGRAFÍA DE TÓRAX
        # ----------------------------------------------------

        "radiografia_torax": """
Create a realistic diagnostic chest X-ray radiograph.

Show a frontal chest radiograph with realistic anatomical
structures including the lungs, ribs, heart and spine.

The image should look like a genuine clinical X-ray used
for university radiology education.

Realistic X-ray grayscale appearance.
Sharp anatomical structures.
Good contrast.
High resolution.

DO NOT add explanatory text.
DO NOT add labels.
DO NOT add arrows.
DO NOT add diagrams.
DO NOT add random objects.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # CONSOLA
        # ----------------------------------------------------

        "consola": """
Create a realistic high-quality photograph of a medical X-ray
radiography control console.

Show a professional radiology workstation used to control
an X-ray examination.

Include realistic monitors, controls, keyboard and medical
equipment.

Professional hospital environment.
Sharp focus.
High detail.

DO NOT add readable text on screens.
DO NOT add labels.
DO NOT add arrows.
DO NOT create a diagram.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # SALA
        # ----------------------------------------------------

        "sala_radiologia": """
Create a realistic photograph of a modern hospital X-ray
radiography room.

Clearly show the complete radiography equipment inside the room,
including the X-ray tube, support structure, radiographic table
and detector.

Professional clinical environment.
Realistic medical equipment.
Sharp focus.
High detail.
Clean hospital room.

DO NOT include patients.
DO NOT add labels.
DO NOT add text.
DO NOT add arrows.
DO NOT create a diagram.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # PARTES
        # ----------------------------------------------------

        "partes_equipo": """
Create a realistic medical photograph showing the main physical
components of a diagnostic X-ray machine arranged clearly in a
professional radiology environment.

Show recognizable components such as:
- X-ray tube
- support arm
- radiographic table
- image detector
- control console

Use realistic medical equipment.

DO NOT add labels.
DO NOT add text.
DO NOT add arrows.
DO NOT create a technical diagram.
DO NOT add watermarks.
""",

        # ----------------------------------------------------
        # GENERAL
        # ----------------------------------------------------

        "general": """
Create a realistic high-quality medical image related specifically
to diagnostic X-ray imaging.

The image should represent the exact subject requested by the user.

Use realistic medical equipment or authentic radiographic imaging
depending on the request.

Professional university radiology reference style.
Sharp focus.
High detail.
Clean composition.

DO NOT add labels.
DO NOT add text.
DO NOT add letters.
DO NOT add arrows.
DO NOT create tables.
DO NOT create comparison charts.
DO NOT create diagrams unless explicitly requested.
DO NOT add watermarks.
"""
    }

    prompt_base = prompts.get(tipo, prompts["general"])

    prompt_final = f"""
{prompt_base}

USER REQUEST:
{pregunta}
"""

    if contexto:
        prompt_final += f"""

PREVIOUS CONVERSATION CONTEXT:
{contexto}

Use the previous context only to understand what the student
is referring to. The current request has priority.
"""

    return prompt_final


# ============================================================
# GENERAR IMAGEN
# ============================================================

def generar_imagen_rx(pregunta, historial=None):

    # --------------------------------------------------------
    # COMPROBAR API
    # --------------------------------------------------------

    if not HF_TOKEN:
        return {
            "ok": False,
            "error": "No se encontró HF_TOKEN en el archivo .env."
        }


    # --------------------------------------------------------
    # COMPROBAR TEMA
    # --------------------------------------------------------

    if not es_tema_rx(pregunta):
        return {
            "ok": False,
            "error": (
                "La generación de imágenes está disponible "
                "únicamente para temas de Rayos X e Imagenología."
            )
        }


    # --------------------------------------------------------
    # DETECTAR TIPO
    # --------------------------------------------------------

    tipo = detectar_tipo_imagen(pregunta)


    # --------------------------------------------------------
    # OBTENER CONTEXTO
    # --------------------------------------------------------

    contexto = obtener_contexto(historial)


    # --------------------------------------------------------
    # CREAR PROMPT
    # --------------------------------------------------------

    prompt = crear_prompt_imagen(
        pregunta,
        tipo,
        contexto
    )


    # --------------------------------------------------------
    # GENERAR
    # --------------------------------------------------------

    try:

        cliente = InferenceClient(
            api_key=HF_TOKEN,
            provider="auto"
        )

        imagen = cliente.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )


        # ----------------------------------------------------
        # CONVERTIR A BASE64
        # ----------------------------------------------------

        buffer = BytesIO()

        imagen.save(
            buffer,
            format="PNG"
        )

        imagen_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")


        # ----------------------------------------------------
        # RESPUESTA
        # ----------------------------------------------------

        return {
            "ok": True,
            "imagen": imagen_base64,
            "mime_type": "image/png",
            "tipo": tipo
        }


    except Exception as e:

        return {
            "ok": False,
            "error": f"Error al generar la imagen: {str(e)}"
        }
from urllib.parse import quote_plus


# ============================================================
# TEMAS RELACIONADOS CON RAYOS X
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
    "detector",
    "detectores",
    "tubo de rayos",
    "tubo de rayos x",
    "ánodo",
    "anodo",
    "cátodo",
    "catodo",
    "atenuación",
    "atenuacion",
    "bremsstrahlung",
    "efecto fotoeléctrico",
    "efecto fotoelectrico",
    "compton",
    "tft",
    "ccd",
    "cmos",
    "cr",
    "radiografía digital",
    "radiografia digital",
    "formación de imagen",
    "formacion de imagen",
    "procesamiento de imágenes",
    "procesamiento de imagen",
    "protección radiológica",
    "proteccion radiologica",
    "seguridad radiológica",
    "seguridad radiologica"
]


# ============================================================
# COMPROBAR SI EL TEMA ES DE RAYOS X
# ============================================================

def es_tema_rx(texto):

    if not texto:
        return False

    texto = texto.lower()

    return any(
        palabra in texto
        for palabra in PALABRAS_RX
    )


# ============================================================
# GENERAR ENLACES DE YOUTUBE
# ============================================================

def generar_videos_rx(pregunta, historial=None):

    if historial is None:
        historial = []

    # --------------------------------------------------------
    # Tomar las últimas conversaciones
    # --------------------------------------------------------

    contexto = ""

    for mensaje in historial[-5:]:

        contexto += (
            f"\nUsuario: {mensaje.get('pregunta', '')}"
            f"\nAsistente: {mensaje.get('respuesta', '')}\n"
        )

    # --------------------------------------------------------
    # Comprobar el tema
    # --------------------------------------------------------

    texto_completo = pregunta + " " + contexto

    if not es_tema_rx(texto_completo):

        return {
            "ok": False,
            "mensaje": (
                "Los videos educativos están disponibles "
                "únicamente para temas relacionados con "
                "Rayos X e Imagenología."
            )
        }

    # --------------------------------------------------------
    # Crear búsquedas
    # --------------------------------------------------------

    busquedas = [

        f"{pregunta} rayos X",

        f"{pregunta} radiología",

        f"{pregunta} imagenología rayos X"

    ]

    enlaces = []

    for busqueda in busquedas:

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(busqueda)
        )

        enlaces.append({

            "titulo": busqueda,

            "url": url

        })

    return {

        "ok": True,

        "enlaces": enlaces

    }
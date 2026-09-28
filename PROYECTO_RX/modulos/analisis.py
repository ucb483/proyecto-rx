# ============================================================
# PLATAFORMA EDUCATIVA DE RAYOS X
# Módulo: Análisis de Imágenes
# ============================================================

import os
import csv
import base64
import io
import numpy as np

from datetime import datetime

from PIL import Image

from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    no_update,
)

import plotly.graph_objects as go


# ============================================================
# PALETA DEL PROYECTO
# ============================================================

THEME = {
    "bg": "#F1F7F3",
    "bg_secondary": "rgb(252, 244, 235)",
    "card": "rgb(255, 251, 247)",
    "green": "#A9D4C0",
    "green_light": "#5E8776",
    "pink": "#5E8776",
    "pink_light": "#2B3A35",
    "mauve": "#A9D4C0",
    "text": "#2B3A35",
    "text_secondary": "#5E8776",
    "border": "#5E8776",
}


# ============================================================
# CARGA DE IMÁGENES
# ============================================================

def decodificar_imagen(contents):
    """
    Convierte una imagen cargada mediante dcc.Upload
    en una matriz NumPy en escala de grises.
    """

    if contents is None:
        return None

    try:
        _, contenido = contents.split(",", 1)

        datos = base64.b64decode(contenido)

        imagen = Image.open(
            io.BytesIO(datos)
        ).convert("L")

        return np.array(
            imagen,
            dtype=np.uint8
        )

    except Exception:
        return None

# ============================================================
# IMÁGENES PROCESADAS GUARDADAS
# ============================================================

def obtener_carpeta_procesadas():
    """
    Devuelve la ruta de la carpeta oficial donde
    Procesamiento guarda las imágenes procesadas.
    """

    return os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ),
        "imagenes_rx",
        "procesadas"
    )


def obtener_imagenes_procesadas():
    """
    Obtiene las imágenes PNG, JPG, JPEG, BMP y TIFF
    disponibles en imagenes_rx/procesadas/.
    """

    carpeta = obtener_carpeta_procesadas()

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    extensiones = (
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tif",
        ".tiff"
    )

    archivos = [
        archivo
        for archivo in os.listdir(carpeta)
        if archivo.lower().endswith(extensiones)
    ]

    archivos.sort(
        key=lambda archivo: os.path.getmtime(
            os.path.join(carpeta, archivo)
        ),
        reverse=True
    )

    return archivos


def obtener_carpeta_originales():
    """Devuelve la carpeta oficial de imágenes originales."""

    return os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ),
        "imagenes_rx",
        "originales"
    )


def obtener_ultima_imagen(carpeta):
    """Devuelve la ruta de la imagen más recientemente guardada."""

    os.makedirs(carpeta, exist_ok=True)

    extensiones = (
        ".png", ".jpg", ".jpeg",
        ".bmp", ".tif", ".tiff"
    )

    archivos = [
        os.path.join(carpeta, archivo)
        for archivo in os.listdir(carpeta)
        if archivo.lower().endswith(extensiones)
    ]

    if not archivos:
        return None

    return max(archivos, key=os.path.getmtime)


def archivo_a_data_uri(ruta):
    """Convierte un archivo de imagen a data URI."""

    if not ruta or not os.path.exists(ruta):
        return None

    extension = os.path.splitext(ruta)[1].lower()

    tipos = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".bmp": "image/bmp",
        ".tif": "image/tiff",
        ".tiff": "image/tiff",
    }

    tipo = tipos.get(extension, "image/png")

    with open(ruta, "rb") as archivo:
        datos = base64.b64encode(archivo.read()).decode()

    return f"data:{tipo};base64,{datos}"

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================

def calcular_estadisticas(imagen):
    """
    Calcula las estadísticas básicas de una imagen.
    """

    imagen = np.asarray(
        imagen,
        dtype=float
    )

    return {
        "media": float(np.mean(imagen)),
        "mediana": float(np.median(imagen)),
        "minimo": float(np.min(imagen)),
        "maximo": float(np.max(imagen)),
        "desviacion_estandar": float(np.std(imagen)),
    }


def calcular_contraste(imagen):
    """
    Calcula el contraste global utilizando
    la desviación estándar de los niveles de gris.
    """

    imagen = np.asarray(
        imagen,
        dtype=float
    )

    return float(np.std(imagen))


def calcular_histograma(imagen):
    """
    Calcula el histograma de niveles de gris.
    """

    histograma, _ = np.histogram(
        imagen.flatten(),
        bins=256,
        range=(0, 256)
    )

    return histograma


# ============================================================
# COMPARACIÓN
# ============================================================

def comparar_imagenes(
    imagen_original,
    imagen_procesada
):
    """
    Compara las estadísticas de la imagen original
    y la imagen procesada.
    """

    estadisticas_original = calcular_estadisticas(
        imagen_original
    )

    estadisticas_procesada = calcular_estadisticas(
        imagen_procesada
    )

    contraste_original = calcular_contraste(
        imagen_original
    )

    contraste_procesada = calcular_contraste(
        imagen_procesada
    )

    return {
        "original": {
            **estadisticas_original,
            "contraste": contraste_original,
        },
        "procesada": {
            **estadisticas_procesada,
            "contraste": contraste_procesada,
        },
    }


# ============================================================
# REPORTE
# ============================================================

def generar_reporte(
    imagen_original,
    imagen_procesada
):
    """
    Genera un reporte textual comparando
    la imagen original y la procesada.
    """

    comparacion = comparar_imagenes(
        imagen_original,
        imagen_procesada
    )

    original = comparacion["original"]
    procesada = comparacion["procesada"]

    reporte = (
        "REPORTE DE ANÁLISIS DE IMAGEN RX\n"
        "====================================\n\n"

        "IMAGEN ORIGINAL\n"
        f"Media: {original['media']:.2f}\n"
        f"Mediana: {original['mediana']:.2f}\n"
        f"Mínimo: {original['minimo']:.2f}\n"
        f"Máximo: {original['maximo']:.2f}\n"
        f"Desviación estándar: "
        f"{original['desviacion_estandar']:.2f}\n"
        f"Contraste: {original['contraste']:.2f}\n\n"

        "IMAGEN PROCESADA\n"
        f"Media: {procesada['media']:.2f}\n"
        f"Mediana: {procesada['mediana']:.2f}\n"
        f"Mínimo: {procesada['minimo']:.2f}\n"
        f"Máximo: {procesada['maximo']:.2f}\n"
        f"Desviación estándar: "
        f"{procesada['desviacion_estandar']:.2f}\n"
        f"Contraste: {procesada['contraste']:.2f}\n\n"

        "CAMBIOS\n"
        f"Δ Media: "
        f"{procesada['media'] - original['media']:.2f}\n"
        f"Δ Mediana: "
        f"{procesada['mediana'] - original['mediana']:.2f}\n"
        f"Δ Desviación estándar: "
        f"{procesada['desviacion_estandar'] - original['desviacion_estandar']:.2f}\n"
        f"Δ Contraste: "
        f"{procesada['contraste'] - original['contraste']:.2f}\n"
    )

    return reporte


# ============================================================
# TARJETA DE ESTADÍSTICA
# ============================================================

def crear_tarjeta_estadistica(
    titulo,
    valor,
    descripcion
):

    return html.Div(
        [
            html.Div(
                titulo,
                style={
                    "fontSize": "10px",
                    "letterSpacing": "1.4px",
                    "fontWeight": "700",
                    "color": THEME["text_secondary"],
                    "marginBottom": "7px",
                },
            ),

            html.Div(
                valor,
                style={
                    "fontSize": "27px",
                    "fontWeight": "800",
                    "color": THEME["text"],
                    "lineHeight": "1.1",
                },
            ),

            html.Div(
                descripcion,
                style={
                    "fontSize": "10px",
                    "color": THEME["text_secondary"],
                    "marginTop": "5px",
                },
            ),
        ],
        style={
            "backgroundColor": THEME["bg_secondary"],
            "border": f"1px solid {THEME['border']}",
            "borderRadius": "12px",
            "padding": "17px",
            "minWidth": "140px",
            "flex": "1",
        },
    )


# ============================================================
# PANEL DE ESTADÍSTICAS
# ============================================================

def crear_panel_estadisticas(
    estadisticas,
    titulo
):

    return html.Div(
        [
            html.Div(
                titulo,
                style={
                    "fontSize": "11px",
                    "letterSpacing": "1.5px",
                    "fontWeight": "800",
                    "color": THEME["pink"],
                    "marginBottom": "13px",
                },
            ),

            html.Div(
                [
                    crear_tarjeta_estadistica(
                        "MEDIA",
                        f"{estadisticas['media']:.2f}",
                        "Intensidad promedio",
                    ),

                    crear_tarjeta_estadistica(
                        "MEDIANA",
                        f"{estadisticas['mediana']:.2f}",
                        "Valor central",
                    ),

                    crear_tarjeta_estadistica(
                        "MÍNIMO",
                        f"{estadisticas['minimo']:.0f}",
                        "Nivel de gris mínimo",
                    ),

                    crear_tarjeta_estadistica(
                        "MÁXIMO",
                        f"{estadisticas['maximo']:.0f}",
                        "Nivel de gris máximo",
                    ),

                    crear_tarjeta_estadistica(
                        "DESV. EST.",
                        f"{estadisticas['desviacion_estandar']:.2f}",
                        "Variación tonal",
                    ),

                    crear_tarjeta_estadistica(
                        "CONTRASTE",
                        f"{estadisticas['contraste']:.2f}",
                        "Contraste global",
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "10px",
                    "flexWrap": "wrap",
                },
            ),
        ],
        style={
            "backgroundColor": THEME["card"],
            "border": f"1px solid {THEME['border']}",
            "borderRadius": "16px",
            "padding": "21px",
            "marginBottom": "20px",
        },
    )


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

def mostrar_analisis():

    return html.Div(
        [

            # ====================================================
            # HERO
            # ====================================================

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "IMAGENOLOGÍA · ANÁLISIS",
                                style={
                                    "fontSize": "10px",
                                    "letterSpacing": "2px",
                                    "fontWeight": "700",
                                    "color": THEME["pink"],
                                    "marginBottom": "12px",
                                },
                            ),

                            html.H1(
                                "Análisis de imágenes RX",
                                style={
                                    "fontSize": "44px",
                                    "fontWeight": "700",
                                    "lineHeight": "1.15",
                                    "letterSpacing": "-1px",
                                    "color": THEME["text"],
                                    "margin": "0 0 15px 0",
                                },
                            ),

                            html.P(
                                "Compara las características estadísticas "
                                "de una radiografía original y una imagen "
                                "procesada para comprender cómo cambian "
                                "sus niveles de gris.",
                                style={
                                    "fontSize": "15px",
                                    "lineHeight": "1.7",
                                    "color": THEME["text_secondary"],
                                    "maxWidth": "760px",
                                    "margin": "0",
                                },
                            ),

                            html.Div(
                                style={
                                    "width": "88px",
                                    "height": "4px",
                                    "backgroundColor": THEME["pink"],
                                    "marginTop": "27px",
                                    "borderRadius": "4px",
                                }
                            ),
                        ],
                        style={
                            "flex": "1",
                        },
                    ),

                    html.Div(
                        [
                            html.Img(
                                src="/assets/interfaz/dente.svg", # <-- Tu imagen
                                alt="Icono de Análisis",
                                style={
                                    "width": "200px",       # Ajusta el tamaño a tu gusto
                                    "height": "auto",
                                    #"opacity": "0.20",      # Lo mantiene como marca de agua sutil
                                    "marginBottom": "5px",  # Separación con el texto de abajo
                                },
                            ),

                            html.Div(
                                "RX · ANALYSIS",
                                style={
                                    "fontSize": "9px",
                                    "letterSpacing": "2px",
                                    "fontWeight": "700",
                                    "color": THEME["green_light"],
                                    "opacity": "0.45",
                                },
                            ),
                        ],
                        style={
                            "width": "180px",
                            "display": "flex",
                            "flexDirection": "column",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "flexShrink": "0",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "space-between",
                    "gap": "30px",
                    "background": "linear-gradient(0deg, rgb(255, 251, 247) 40%, rgb(169, 212, 192) 100%)",
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "18px",
                    "padding": "34px 38px",
                    "minHeight": "235px",
                    "boxSizing": "border-box",
                    "marginBottom": "24px",
                },
            ),

            # ====================================================
            # EXPLICACIÓN
            # ====================================================

            html.Div(
                [
                    html.Div(
                        "¿QUÉ ANALIZAMOS?",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "8px",
                        },
                    ),

                    html.P(
                        "El análisis utiliza estadísticas de intensidad "
                        "para comparar la imagen original con la procesada. "
                        "La desviación estándar se utiliza como medida "
                        "del contraste global.",
                        style={
                            "fontSize": "13px",
                            "lineHeight": "1.7",
                            "color": THEME["text_secondary"],
                            "margin": "0",
                        },
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "16px",
                    "padding": "20px 24px",
                    "marginBottom": "20px",
                },
            ),

            # ====================================================
            # CARGA DE IMÁGENES
            # ====================================================

            html.Div(
                [
                    html.Div(
                        "CARGAR IMÁGENES PARA COMPARAR",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "5px",
                        },
                    ),

                    html.P(
                        "Puedes utilizar una radiografía original "
                        "y su versión procesada.",
                        style={
                            "fontSize": "12px",
                            "color": THEME["text_secondary"],
                            "margin": "0 0 16px 0",
                        },
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "IMAGEN ORIGINAL",
                                        style={
                                            "fontSize": "10px",
                                            "letterSpacing": "1.3px",
                                            "fontWeight": "700",
                                            "color": THEME["text_secondary"],
                                            "marginBottom": "8px",
                                        },
                                    ),
                                    dcc.Upload(
                                        id="analisis-upload-original",
                                        children=html.Div(
                                            [
                                                html.Div(
                                                    "🩻",
                                                    style={
                                                        "fontSize": "28px",
                                                        "marginBottom": "5px",
                                                    },
                                                ),
                                                html.Div(
                                                    "Seleccionar RX original",
                                                    style={
                                                        "fontWeight": "700",
                                                        "color": THEME["text"],
                                                    },
                                                ),
                                                html.Div(
                                                    "PNG · JPG · JPEG · BMP · TIFF",
                                                    style={
                                                        "fontSize": "10px",
                                                        "color": THEME["text_secondary"],
                                                        "marginTop": "5px",
                                                    },
                                                ),
                                            ],
                                            style={"textAlign": "center"},
                                        ),
                                        style={
                                            "height": "250px",
                                            "borderWidth": "1.5px",
                                            "borderStyle": "dashed",
                                            "borderColor": THEME["green_light"],
                                            "borderRadius": "12px",
                                            "backgroundColor": "rgb(252, 244, 235)",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "cursor": "pointer",
                                            "overflow": "hidden",
                                        },
                                        multiple=False,
                                    ),
                                ],
                                style={
                                    "flex": "1",
                                    "minWidth": "300px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "IMAGEN PROCESADA",
                                        style={
                                            "fontSize": "10px",
                                            "letterSpacing": "1.3px",
                                            "fontWeight": "700",
                                            "color": THEME["pink"],
                                            "marginBottom": "8px",
                                        },
                                    ),
                                    dcc.Upload(
                                        id="analisis-upload-procesada",
                                        children=html.Div(
                                            [
                                                html.Div(
                                                    "✦",
                                                    style={
                                                        "fontSize": "28px",
                                                        "color": THEME["pink"],
                                                        "marginBottom": "5px",
                                                    },
                                                ),
                                                html.Div(
                                                    "Seleccionar RX procesada",
                                                    style={
                                                        "fontWeight": "700",
                                                        "color": THEME["text"],
                                                    },
                                                ),
                                                html.Div(
                                                    "PNG · JPG · JPEG · BMP · TIFF",
                                                    style={
                                                        "fontSize": "10px",
                                                        "color": THEME["text_secondary"],
                                                        "marginTop": "5px",
                                                    },
                                                ),
                                            ],
                                            style={"textAlign": "center"},
                                        ),
                                        style={
                                            "height": "250px",
                                            "borderWidth": "1.5px",
                                            "borderStyle": "dashed",
                                            "borderColor": THEME["pink"],
                                            "borderRadius": "12px",
                                            "backgroundColor": "rgb(252, 244, 235)",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "cursor": "pointer",
                                            "overflow": "hidden",
                                        },
                                        multiple=False,
                                    ),
                                ],
                                style={
                                    "flex": "1",
                                    "minWidth": "300px",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "gap": "18px",
                            "flexWrap": "wrap",
                        },
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "16px",
                    "padding": "22px 24px",
                    "marginBottom": "20px",
                },
            ),

            # ====================================================
            # ESTADÍSTICAS
            # ====================================================

            html.Div(
                id="analisis-estadisticas",
                children=html.Div(
                    "Carga las dos imágenes para visualizar "
                    "sus estadísticas.",
                    style={
                        "color": THEME["text_secondary"],
                        "fontSize": "12px",
                    },
                ),
                style={
                    "marginBottom": "20px",
                },
            ),

            # ====================================================
            # HISTOGRAMA
            # ====================================================

            html.Div(
                [
                    html.Div(
                        "DISTRIBUCIÓN DE NIVELES DE GRIS",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["green_light"],
                            "marginBottom": "7px",
                        },
                    ),

                    html.H3(
                        "📊 Comparación de histogramas",
                        style={
                            "margin": "0 0 6px 0",
                            "fontSize": "28px",
                            "fontWeight": "800",
                            "color": THEME["text"],
                        },
                    ),

                    html.P(
                        "Observa cómo cambia la distribución de "
                        "intensidades después del procesamiento.",
                        style={
                            "color": THEME["text_secondary"],
                            "fontSize": "12px",
                            "margin": "0 0 16px 0",
                        },
                    ),

                    dcc.Graph(
                        id="analisis-histograma",
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                        style={
                            "height": "390px",
                        },
                    ),
                ],
                style={
                    "background": (
                        f"linear-gradient(145deg, "
                        f"{THEME['card']} 0%, "
                        f"{THEME['bg_secondary']} 100%)"
                    ),
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "18px",
                    "padding": "24px 26px",
                    "marginBottom": "20px",
                    "overflow": "hidden",
                },
            ),

            # ====================================================
            # INTERPRETACIÓN
            # ====================================================

            html.Div(
                [
                    html.Div(
                        "INTERPRETACIÓN",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "9px",
                        },
                    ),

                    html.Div(
                        id="analisis-interpretacion",
                        children=(
                            "Carga ambas imágenes para obtener "
                            "una comparación estadística."
                        ),
                        style={
                            "fontSize": "13px",
                            "lineHeight": "1.7",
                            "color": THEME["text_secondary"],
                        },
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "16px",
                    "padding": "21px 24px",
                    "marginBottom": "20px",
                },
            ),

            # ====================================================
            # REPORTE
            # ====================================================

            html.Div(
                [
                    html.Div(
                        "REPORTE",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["green_light"],
                            "marginBottom": "9px",
                        },
                    ),

                    html.Button(
                        "📄 Generar reporte",
                        id="btn-generar-reporte",
                        n_clicks=0,
                        style={
                            "backgroundColor": THEME["green"],
                            "color": THEME["text"],
                            "border": f"1px solid {THEME['border']}",
                            "borderRadius": "10px",
                            "padding": "11px 20px",
                            "fontSize": "13px",
                            "fontWeight": "700",
                            "cursor": "pointer",
                        },
                    ),

                    dcc.Download(
                        id="analisis-download-reporte"
                    ),

                    html.Div(
                        id="analisis-reporte",
                        style={
                            "marginTop": "15px",
                            "whiteSpace": "pre-wrap",
                            "fontFamily": "monospace",
                            "fontSize": "11px",
                            "lineHeight": "1.6",
                            "color": THEME["text_secondary"],
                        },
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "16px",
                    "padding": "21px 24px",
                    "marginBottom": "30px",
                },
            ),

            dcc.Store(
                id="analisis-carga-inicial",
                data=1,
            ),

        ],
        style={
            "backgroundColor": THEME["bg"],
            "minHeight": "100vh",
            "padding": "30px",
            "boxSizing": "border-box",
        },
    )


# ============================================================
# ACTIVIDADES DE RAYOS X
# ============================================================

PREGUNTAS_RX = [

    {
        "pregunta": "¿Qué tipo de radiación son los rayos X?",
        "opciones": [
            "Radiación sonora",
            "Radiación electromagnética ionizante",
            "Radiación mecánica",
            "Radiación no ionizante",
        ],
        "correcta": 1,
        "explicacion": (
            "Los rayos X son ondas electromagnéticas de alta "
            "frecuencia y forman parte de la radiación ionizante."
        ),
    },

    {
        "pregunta": (
            "¿Qué ocurre con el fotón incidente en "
            "el efecto fotoeléctrico?"
        ),
        "opciones": [
            "Cambia de dirección pero conserva toda su energía",
            "Se convierte en luz visible",
            "Es completamente absorbido por el átomo",
            "No interactúa con el átomo",
        ],
        "correcta": 2,
        "explicacion": (
            "En el efecto fotoeléctrico, el fotón incidente "
            "es completamente absorbido y se expulsa un electrón."
        ),
    },

    {
        "pregunta": "¿Qué ocurre en la dispersión Compton?",
        "opciones": [
            "El fotón es completamente absorbido",
            "El fotón pierde energía y cambia de dirección",
            "El fotón aumenta su energía",
            "El fotón desaparece sin interacción",
        ],
        "correcta": 1,
        "explicacion": (
            "En Compton, el fotón transfiere parte de su energía "
            "a un electrón, pierde energía y cambia de dirección."
        ),
    },

    {
        "pregunta": (
            "¿Cuál es la principal fuente de rayos X "
            "producidos en un tubo de rayos X?"
        ),
        "opciones": [
            "Radiación ultravioleta",
            "Efecto fotoeléctrico",
            "Bremsstrahlung",
            "Dispersión Rayleigh",
        ],
        "correcta": 2,
        "explicacion": (
            "La radiación Bremsstrahlung es la fuente principal "
            "de rayos X producidos por un tubo de rayos X."
        ),
    },

    {
        "pregunta": (
            "Aproximadamente, ¿qué porcentaje de la energía "
            "depositada por los electrones en el ánodo se "
            "convierte en rayos X?"
        ),
        "opciones": [
            "1 %",
            "10 %",
            "50 %",
            "99 %",
        ],
        "correcta": 0,
        "explicacion": (
            "Las diapositivas indican que aproximadamente el 1 % "
            "de la energía se convierte en rayos X y el 99 % "
            "restante se convierte en calor."
        ),
    },

    {
        "pregunta": (
            "¿Qué describe la atenuación de un haz de rayos X?"
        ),
        "opciones": [
            "El aumento de intensidad del haz",
            "La pérdida de fuerza del haz",
            "La generación de luz visible",
            "El aumento de la frecuencia",
        ],
        "correcta": 1,
        "explicacion": (
            "La atenuación describe la pérdida de fuerza de un "
            "haz de radiación electromagnética al atravesar "
            "un material."
        ),
    },

    {
        "pregunta": (
            "¿Qué significa un valor alto del coeficiente "
            "de atenuación lineal μ?"
        ),
        "opciones": [
            "El tejido absorbe los rayos X de manera eficiente",
            "El tejido no interactúa con los rayos X",
            "Todos los rayos X atraviesan el tejido",
            "El detector deja de funcionar",
        ],
        "correcta": 0,
        "explicacion": (
            "Un valor alto de μ corresponde a una absorción "
            "eficiente de rayos X, por lo que llegan menos "
            "rayos X al detector."
        ),
    },

    {
        "pregunta": (
            "¿Cuál es una diferencia entre un detector TFT "
            "indirecto y uno directo?"
        ),
        "opciones": [
            "El indirecto convierte primero los rayos X en luz",
            "El directo siempre utiliza película",
            "El indirecto no detecta rayos X",
            "No existe ninguna diferencia",
        ],
        "correcta": 0,
        "explicacion": (
            "Los TFT de conversión indirecta utilizan un "
            "centelleador para convertir los rayos X en luz. "
            "Los de conversión directa convierten la energía "
            "de los rayos X directamente en carga."
        ),
    },
]


# ============================================================
# CORREGIR ACTIVIDAD
# ============================================================

def corregir_actividad(respuestas):

    aciertos = 0
    resultados = []

    for i, respuesta in enumerate(respuestas):

        pregunta = PREGUNTAS_RX[i]
        correcta = pregunta["correcta"]

        if respuesta == correcta:

            aciertos += 1

            resultados.append(
                {
                    "correcta": True,
                    "explicacion": (
                        "✓ Correcto. "
                        + pregunta["explicacion"]
                    ),
                }
            )

        else:

            resultados.append(
                {
                    "correcta": False,
                    "explicacion": (
                        "✗ Incorrecto. "
                        "La respuesta correcta es: "
                        + pregunta["opciones"][correcta]
                        + ". "
                        + pregunta["explicacion"]
                    ),
                }
            )

    puntaje = (
        aciertos / len(PREGUNTAS_RX)
    ) * 100

    return (
        aciertos,
        puntaje,
        resultados
    )


# ============================================================
# GUARDAR RESULTADO
# ============================================================

def guardar_resultado_actividad(
    nombre,
    puntaje
):

    carpeta = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "resultados",
    )

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    ruta_csv = os.path.join(
        carpeta,
        "resultados_estudiantes.csv"
    )

    archivo_nuevo = not os.path.exists(
        ruta_csv
    )

    with open(
        ruta_csv,
        "a",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.writer(archivo)

        if archivo_nuevo:

            escritor.writerow(
                [
                    "nombre",
                    "fecha",
                    "actividad",
                    "puntaje",
                ]
            )

        escritor.writerow(
            [
                nombre,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Actividad Rayos X",
                round(puntaje, 2),
            ]
        )


# ============================================================
# CALLBACKS
# ============================================================

def registrar_callbacks(app):

    # ========================================================
    # CARGA AUTOMÁTICA DE LA ÚLTIMA PAREJA
    # ========================================================

    @app.callback(
        Output("analisis-upload-original", "contents"),
        Output("analisis-upload-procesada", "contents"),
        Input("analisis-carga-inicial", "data"),
        prevent_initial_call=False,
    )
    def cargar_ultima_pareja(_):

        ruta_original = obtener_ultima_imagen(
            obtener_carpeta_originales()
        )

        ruta_procesada = obtener_ultima_imagen(
            obtener_carpeta_procesadas()
        )

        return (
            archivo_a_data_uri(ruta_original),
            archivo_a_data_uri(ruta_procesada),
        )


    # ========================================================
    # MOSTRAR IMAGEN ORIGINAL EN SU CUADRO
    # ========================================================

    @app.callback(
        Output("analisis-upload-original", "children"),
        Input("analisis-upload-original", "contents"),
    )
    def mostrar_original(contents):

        if contents is None:
            return html.Div(
                [
                    html.Div(
                        "🩻",
                        style={
                            "fontSize": "28px",
                            "marginBottom": "5px",
                        },
                    ),
                    html.Div(
                        "Seleccionar RX original",
                        style={
                            "fontWeight": "700",
                            "color": THEME["text"],
                        },
                    ),
                    html.Div(
                        "PNG · JPG · JPEG · BMP · TIFF",
                        style={
                            "fontSize": "10px",
                            "color": THEME["text_secondary"],
                            "marginTop": "5px",
                        },
                    ),
                ],
                style={"textAlign": "center"},
            )

        return html.Img(
            src=contents,
            style={
                "maxWidth": "100%",
                "maxHeight": "235px",
                "objectFit": "contain",
            },
        )


    # ========================================================
    # MOSTRAR IMAGEN PROCESADA EN SU CUADRO
    # ========================================================

    @app.callback(
        Output("analisis-upload-procesada", "children"),
        Input("analisis-upload-procesada", "contents"),
    )
    def mostrar_procesada(contents):

        if contents is None:
            return html.Div(
                [
                    html.Div(
                        "✦",
                        style={
                            "fontSize": "28px",
                            "color": THEME["pink"],
                            "marginBottom": "5px",
                        },
                    ),
                    html.Div(
                        "Seleccionar RX procesada",
                        style={
                            "fontWeight": "700",
                            "color": THEME["text"],
                        },
                    ),
                    html.Div(
                        "PNG · JPG · JPEG · BMP · TIFF",
                        style={
                            "fontSize": "10px",
                            "color": THEME["text_secondary"],
                            "marginTop": "5px",
                        },
                    ),
                ],
                style={"textAlign": "center"},
            )

        return html.Img(
            src=contents,
            style={
                "maxWidth": "100%",
                "maxHeight": "235px",
                "objectFit": "contain",
            },
        )


    # ========================================================
    # ANÁLISIS COMPLETO
    # ========================================================

    @app.callback(
        Output("analisis-estadisticas", "children"),
        Output("analisis-histograma", "figure"),
        Output("analisis-interpretacion", "children"),
        Input("analisis-upload-original", "contents"),
        Input("analisis-upload-procesada", "contents"),
    )
    def analizar_imagenes(contents_original, contents_procesada):

        figura = go.Figure()

        figura.update_layout(
            paper_bgcolor=THEME["bg_secondary"],
            plot_bgcolor=THEME["bg_secondary"],
            font={
                "family": "'Lora', Georgia, serif",
                "color": THEME["text"],
            },
            xaxis={
                "title": "Nivel de gris",
                "range": [0, 255],
                "fixedrange": True,
            },
            yaxis={
                "title": "Frecuencia",
                "fixedrange": True,
            },
            height=390,
            margin={"l": 60, "r": 25, "t": 30, "b": 55},
        )

        if contents_original is None or contents_procesada is None:
            return (
                html.Div(
                    "Carga ambas imágenes para realizar el análisis.",
                    style={
                        "color": THEME["text_secondary"],
                        "fontSize": "12px",
                    },
                ),
                figura,
                "Esperando las dos imágenes.",
            )

        imagen_original = decodificar_imagen(contents_original)
        imagen_procesada = decodificar_imagen(contents_procesada)

        if imagen_original is None or imagen_procesada is None:
            return (
                html.Div(
                    "No se pudo leer una de las imágenes.",
                    style={
                        "color": THEME["pink_light"],
                        "fontSize": "12px",
                    },
                ),
                figura,
                "No fue posible realizar el análisis.",
            )

        comparacion = comparar_imagenes(
            imagen_original,
            imagen_procesada,
        )

        original = comparacion["original"]
        procesada = comparacion["procesada"]

        estadisticas = html.Div(
            [
                crear_panel_estadisticas(
                    original,
                    "IMAGEN ORIGINAL",
                ),
                crear_panel_estadisticas(
                    procesada,
                    "IMAGEN PROCESADA",
                ),
            ]
        )

        hist_original = calcular_histograma(imagen_original)
        hist_procesada = calcular_histograma(imagen_procesada)

        figura.add_trace(
            go.Scatter(
                x=list(range(256)),
                y=hist_original,
                mode="lines",
                name="Original",
                line={"color": "#D97D77", "width": 2.5},
                hovertemplate=(
                    "Nivel de gris: %{x}<br>"
                    "Frecuencia: %{y:,}<extra>Original</extra>"
                ),
            )
        )

        figura.add_trace(
            go.Scatter(
                x=list(range(256)),
                y=hist_procesada,
                mode="lines",
                name="Procesada",
                line={"color": "#E0B96B", "width": 2.5},
                hovertemplate=(
                    "Nivel de gris: %{x}<br>"
                    "Frecuencia: %{y:,}<extra>Procesada</extra>"
                ),
            )
        )

        figura.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.01,
                "xanchor": "right",
                "x": 1,
            },
            hoverlabel={
                "bgcolor": THEME["bg"],
                "bordercolor": THEME["border"],
                "font": {"color": THEME["text"]},
            },
        )

        cambio_media = procesada["media"] - original["media"]
        cambio_contraste = (
            procesada["contraste"] - original["contraste"]
        )
        cambio_desviacion = (
            procesada["desviacion_estandar"]
            - original["desviacion_estandar"]
        )

        if cambio_contraste > 0:
            texto_contraste = (
                "El contraste global aumentó "
                f"en {abs(cambio_contraste):.2f}."
            )
        elif cambio_contraste < 0:
            texto_contraste = (
                "El contraste global disminuyó "
                f"en {abs(cambio_contraste):.2f}."
            )
        else:
            texto_contraste = (
                "El contraste global no presentó un cambio apreciable."
            )

        interpretacion = html.Div(
            [
                html.P(
                    [
                        html.Strong(
                            "Media: ",
                            style={"color": THEME["text"]},
                        ),
                        f"cambió en {cambio_media:.2f} niveles de gris.",
                    ],
                    style={"marginTop": "0"},
                ),
                html.P(texto_contraste),
                html.P(
                    [
                        html.Strong(
                            "Desviación estándar: ",
                            style={"color": THEME["text"]},
                        ),
                        f"cambió en {cambio_desviacion:.2f}.",
                    ]
                ),
                html.P(
                    "Estos valores permiten describir estadísticamente "
                    "cómo cambió la distribución de intensidades de la "
                    "imagen después del procesamiento."
                ),
            ]
        )

        return estadisticas, figura, interpretacion


    # ========================================================
    # GENERAR REPORTE
    # ========================================================

    @app.callback(
        Output("analisis-reporte", "children"),
        Input("btn-generar-reporte", "n_clicks"),
        State("analisis-upload-original", "contents"),
        State("analisis-upload-procesada", "contents"),
        prevent_initial_call=True,
    )
    def mostrar_reporte(
        n_clicks,
        contents_original,
        contents_procesada,
    ):

        if contents_original is None or contents_procesada is None:
            return (
                "Carga primero la imagen original y la imagen procesada."
            )

        imagen_original = decodificar_imagen(contents_original)
        imagen_procesada = decodificar_imagen(contents_procesada)

        if imagen_original is None or imagen_procesada is None:
            return "No se pudo leer una de las imágenes."

        return generar_reporte(
            imagen_original,
            imagen_procesada,
        )


    # ========================================================
    # DESCARGAR REPORTE
    # ========================================================

    @app.callback(
        Output("analisis-download-reporte", "data"),
        Input("btn-generar-reporte", "n_clicks"),
        State("analisis-upload-original", "contents"),
        State("analisis-upload-procesada", "contents"),
        prevent_initial_call=True,
    )
    def descargar_reporte(
        n_clicks,
        contents_original,
        contents_procesada,
    ):

        if contents_original is None or contents_procesada is None:
            return no_update

        imagen_original = decodificar_imagen(contents_original)
        imagen_procesada = decodificar_imagen(contents_procesada)

        if imagen_original is None or imagen_procesada is None:
            return no_update

        reporte = generar_reporte(
            imagen_original,
            imagen_procesada,
        )

        return dcc.send_string(
            reporte,
            "reporte_analisis_rx.txt",
        )


# ============================================================
# INTERFAZ DE ACTIVIDADES
# ============================================================

def mostrar_actividades():

    componentes = [

        html.Div(
            "IMAGENOLOGÍA · ACTIVIDADES",
            style={
                "fontSize": "10px",
                "letterSpacing": "2px",
                "fontWeight": "700",
                "color": THEME["pink"],
                "marginBottom": "12px",
            },
        ),

        html.H1(
            "Actividades de Rayos X",
            style={
                "fontSize": "42px",
                "fontWeight": "700",
                "color": THEME["text"],
                "margin": "0 0 12px 0",
            },
        ),

        html.P(
            "Comprueba lo aprendido sobre los fundamentos "
            "de los Rayos X.",
            style={
                "fontSize": "14px",
                "lineHeight": "1.7",
                "color": THEME["text_secondary"],
                "marginBottom": "25px",
            },
        ),

        html.Div(
            [
                html.Label(
                    "Nombre del estudiante",
                    style={
                        "fontWeight": "700",
                        "fontSize": "13px",
                        "color": THEME["text"],
                        "display": "block",
                        "marginBottom": "8px",
                    },
                ),

                dcc.Input(
                    id="nombre-estudiante",
                    type="text",
                    placeholder="Escribe tu nombre",
                    style={
                        "width": "100%",
                        "boxSizing": "border-box",
                        "padding": "11px 13px",
                        "borderRadius": "9px",
                        "border": (
                            f"1px solid {THEME['border']}"
                        ),
                        "backgroundColor": THEME[
                            "bg_secondary"
                        ],
                        "color": THEME["text"],
                        "marginBottom": "25px",
                    },
                ),
            ]
        ),
    ]

    for i, pregunta in enumerate(PREGUNTAS_RX):

        componentes.append(
            html.Div(
                [
                    html.Div(
                        f"PREGUNTA {i + 1}",
                        style={
                            "fontSize": "9px",
                            "letterSpacing": "1.5px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "7px",
                        },
                    ),

                    html.H4(
                        pregunta["pregunta"],
                        style={
                            "fontSize": "15px",
                            "lineHeight": "1.5",
                            "color": THEME["text"],
                            "margin": "0 0 13px 0",
                        },
                    ),

                    dcc.RadioItems(
                        id=f"respuesta-{i}",
                        options=[
                            {
                                "label": opcion,
                                "value": j,
                            }
                            for j, opcion
                            in enumerate(
                                pregunta["opciones"]
                            )
                        ],
                        value=None,
                        labelStyle={
                            "display": "block",
                            "padding": "7px 0",
                            "color": THEME[
                                "text_secondary"
                            ],
                            "fontSize": "13px",
                        },
                        inputStyle={
                            "marginRight": "8px",
                        },
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": (
                        f"1px solid {THEME['border']}"
                    ),
                    "borderRadius": "14px",
                    "padding": "20px",
                    "marginBottom": "15px",
                },
            )
        )

    componentes.extend(
        [
            html.Button(
                "✓  Calificar actividad",
                id="btn-calificar-actividad",
                n_clicks=0,
                style={
                    "backgroundColor": THEME["green"],
                    "color": THEME["text"],
                    "border": (
                        f"1px solid {THEME['border']}"
                    ),
                    "borderRadius": "10px",
                    "padding": "12px 24px",
                    "fontSize": "13px",
                    "fontWeight": "700",
                    "cursor": "pointer",
                },
            ),

            html.Div(
                id="resultado-actividad",
                style={
                    "marginTop": "22px",
                },
            ),
        ]
    )

    return html.Div(
        componentes,
        style={
            "backgroundColor": THEME["bg"],
            "minHeight": "100vh",
            "padding": "30px",
            "boxSizing": "border-box",
        },
    )


# ============================================================
# CALLBACK DE ACTIVIDAD
# ============================================================

def registrar_callbacks_actividades(app):

    @app.callback(
        Output(
            "resultado-actividad",
            "children"
        ),

        Input(
            "btn-calificar-actividad",
            "n_clicks"
        ),

        State(
            "nombre-estudiante",
            "value"
        ),

        *[
            State(
                f"respuesta-{i}",
                "value"
            )
            for i in range(len(PREGUNTAS_RX))
        ],

        prevent_initial_call=True,
    )
    def calificar(
        n_clicks,
        nombre,
        *respuestas
    ):

        if not nombre or not nombre.strip():

            return html.Div(
                "Escribe tu nombre antes de calificar.",
                style={
                    "color": THEME["pink_light"],
                    "fontSize": "13px",
                },
            )

        if any(
            respuesta is None
            for respuesta in respuestas
        ):

            return html.Div(
                "Responde todas las preguntas antes "
                "de calificar.",
                style={
                    "color": THEME["pink_light"],
                    "fontSize": "13px",
                },
            )

        aciertos, puntaje, resultados = (
            corregir_actividad(
                respuestas
            )
        )

        guardar_resultado_actividad(
            nombre.strip(),
            puntaje
        )

        elementos = [

            html.Div(
                [
                    html.Div(
                        "RESULTADO",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                        },
                    ),

                    html.Div(
                        f"{puntaje:.1f} %",
                        style={
                            "fontSize": "42px",
                            "fontWeight": "800",
                            "color": THEME["text"],
                            "marginTop": "5px",
                        },
                    ),

                    html.Div(
                        f"{aciertos} de "
                        f"{len(PREGUNTAS_RX)} respuestas correctas",
                        style={
                            "fontSize": "12px",
                            "color": THEME[
                                "text_secondary"
                            ],
                        },
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": (
                        f"1px solid {THEME['border']}"
                    ),
                    "borderRadius": "14px",
                    "padding": "20px",
                    "marginBottom": "15px",
                },
            )
        ]

        for i, resultado in enumerate(
            resultados
        ):

            elementos.append(
                html.Div(
                    [
                        html.Div(
                            f"{'✓' if resultado['correcta'] else '✗'} "
                            f"Pregunta {i + 1}",
                            style={
                                "fontWeight": "700",
                                "color": THEME["text"],
                                "marginBottom": "5px",
                            },
                        ),

                        html.Div(
                            resultado["explicacion"],
                            style={
                                "fontSize": "12px",
                                "lineHeight": "1.6",
                                "color": THEME[
                                    "text_secondary"
                                ],
                            },
                        ),
                    ],
                    style={
                        "backgroundColor": THEME[
                            "bg_secondary"
                        ],
                        "border": (
                            f"1px solid "
                            f"{THEME['border']}"
                        ),
                        "borderRadius": "10px",
                        "padding": "13px",
                        "marginBottom": "9px",
                    },
                )
            )

        return elementos
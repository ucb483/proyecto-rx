import base64
import io
import os

import numpy as np
from PIL import Image

from dash import dcc, html, Input, Output, State
from scipy.ndimage import correlate1d, gaussian_filter, median_filter
from skimage import exposure
from skimage.filters import sobel
from skimage.restoration import denoise_bilateral

import plotly.graph_objects as go


# ============================================================
# PALETA DEL PROYECTO
# ============================================================

THEME = {
    "bg": "#F1F7F3",
    "bg_secondary": "rgb(255, 251, 247)",
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


# Conversión del ClipLimit estilo OpenCV (0.5 - 10) al clip_limit
# normalizado de scikit-image (0 - 1).
CLIP_ESCALA_OPENCV = 256.0


# ============================================================
# CARGA Y CONVERSIÓN DE IMÁGENES
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


def convertir_grises(IM):
    """
    Convierte una imagen a escala de grises.
    """

    if IM is None:
        return None

    if IM.ndim == 2:
        return IM.astype(np.uint8)

    imagen = Image.fromarray(IM)

    imagen = imagen.convert("L")

    return np.array(
        imagen,
        dtype=np.uint8
    )


# ============================================================
# MÉTODOS DE PROCESAMIENTO
# ============================================================

def ajustar_brillo(IM, valor_brillo):
    """
    Ajusta el brillo de la imagen.
    """

    if IM is None:
        return None

    resultado = np.clip(
        IM.astype(np.int16) + int(valor_brillo),
        0,
        255
    ).astype(np.uint8)

    return resultado


def ajustar_contraste(IM, valor_contraste):
    """
    Ajusta el contraste de la imagen.
    """

    if IM is None:
        return None

    resultado = np.clip(
        IM.astype(np.float32) * float(valor_contraste),
        0,
        255
    ).astype(np.uint8)

    return resultado


def aplicar_brillo_y_contraste(
    IM,
    valor_brillo,
    valor_contraste
):
    """
    Aplica primero brillo y posteriormente contraste.

    Se corrige el problema del código original de Integrante 4,
    donde la segunda operación volvía a utilizar la imagen
    original y descartaba el ajuste de brillo.
    """

    if IM is None:
        return None

    imagen = ajustar_brillo(
        IM,
        valor_brillo
    )

    imagen = ajustar_contraste(
        imagen,
        valor_contraste
    )

    return imagen


def ecualizar_histograma(IM):
    """
    Ecualización global del histograma (GHE).
    """

    if IM is None:
        return None

    resultado = exposure.equalize_hist(IM)

    resultado = np.clip(
        resultado * 255,
        0,
        255
    ).astype(np.uint8)

    return resultado


def ecualizar_clahe(
    IM,
    clip_limit=2.0,
    tile_grid=8
):
    """
    Ecualización adaptativa CLAHE.

    Parámetros (misma convención que OpenCV / proyecto base):
    - clip_limit: límite de contraste (0.5 - 10).
    - tile_grid : número de regiones por lado (tile_grid x tile_grid).
    """

    if IM is None:
        return None

    alto, ancho = IM.shape[:2]

    grid = max(int(tile_grid), 1)

    # skimage espera el tamaño de cada región EN PÍXELES,
    # no el número de regiones por lado.
    kernel_size = (
        max(alto // grid, 1),
        max(ancho // grid, 1)
    )

    resultado = exposure.equalize_adapthist(
        IM,
        clip_limit=float(clip_limit) / CLIP_ESCALA_OPENCV,
        kernel_size=kernel_size
    )

    resultado = np.clip(
        resultado * 255,
        0,
        255
    ).astype(np.uint8)

    return resultado


def aplicar_gamma(IM, gamma):
    """
    Corrección gamma.
    """

    if IM is None:
        return None

    gamma = float(gamma)

    if gamma <= 0:
        gamma = 1.0

    imagen_normalizada = (
        IM.astype(np.float32) / 255.0
    )

    resultado = np.power(
        imagen_normalizada,
        gamma
    )

    resultado = np.clip(
        resultado * 255,
        0,
        255
    ).astype(np.uint8)

    return resultado


# Rango permitido del kernel para cada filtro (mínimo, máximo).
RANGO_KERNEL = {
    "Gaussiano": (3, 15),
    "Mediana": (3, 9),
    "Bilateral": (3, 15),
    "Sobel": (1, 7),
}


def normalizar_kernel(filtro, ksize):
    """
    Devuelve un kernel entero, impar y dentro del rango del filtro.
    """

    minimo, maximo = RANGO_KERNEL.get(filtro, (3, 15))

    k = int(round(float(ksize)))

    if k % 2 == 0:
        k += 1

    return max(minimo, min(k, maximo))


def _kernels_sobel(k):
    """
    Kernels 1D del operador Sobel de apertura k (1, 3, 5 o 7),
    equivalentes a cv2.getDerivKernels.

    Devuelve (suavizado, derivada).
    """

    if k <= 1:
        return (
            np.array([1.0]),
            np.array([-1.0, 0.0, 1.0])
        )

    suavizado = np.array([1.0])

    for _ in range(k - 1):
        suavizado = np.convolve(suavizado, [1.0, 1.0])

    base = np.array([1.0])

    for _ in range(k - 3):
        base = np.convolve(base, [1.0, 1.0])

    derivada = np.convolve(base, [-1.0, 0.0, 1.0])

    return suavizado, derivada


def aplicar_filtro(
    IM,
    filtro,
    ksize=5
):
    """
    Aplica el filtro seleccionado usando el tamaño de kernel indicado.

    Filtros:
    - Ninguno
    - Gaussiano : ventana ksize x ksize
    - Mediana   : ventana ksize x ksize
    - Bilateral : ksize = diámetro de la vecindad
    - Sobel     : ksize = apertura del operador (1, 3, 5, 7)
    """

    if IM is None:
        return None

    if filtro == "Ninguno":
        return IM.copy()

    # --------------------------------------------------------
    # GAUSSIANO
    # --------------------------------------------------------

    if filtro == "Gaussiano":

        k = normalizar_kernel(filtro, ksize)

        # Misma sigma que usa OpenCV cuando sigma = 0
        sigma = 0.3 * ((k - 1) * 0.5 - 1) + 0.8

        resultado = gaussian_filter(
            IM.astype(np.float32),
            sigma=sigma,
            truncate=(k // 2) / sigma,   # ventana de exactamente k x k
            mode="mirror"
        )

        return np.clip(
            np.rint(resultado),
            0,
            255
        ).astype(np.uint8)

    # --------------------------------------------------------
    # MEDIANA
    # --------------------------------------------------------

    if filtro == "Mediana":

        k = normalizar_kernel(filtro, ksize)

        resultado = median_filter(
            IM,
            size=k,
            mode="mirror"
        )

        return np.clip(
            resultado,
            0,
            255
        ).astype(np.uint8)

    # --------------------------------------------------------
    # BILATERAL
    # --------------------------------------------------------

    if filtro == "Bilateral":

        d = normalizar_kernel(filtro, ksize)

        resultado = denoise_bilateral(
            IM,
            win_size=d,
            sigma_color=0.05,
            sigma_spatial=max(d / 2.0, 1.0),
            channel_axis=None
        )

        return np.clip(
            resultado * 255,
            0,
            255
        ).astype(np.uint8)

    # --------------------------------------------------------
    # SOBEL
    # --------------------------------------------------------

    if filtro == "Sobel":

        k = normalizar_kernel(filtro, ksize)

        suavizado, derivada = _kernels_sobel(k)

        img = IM.astype(np.float32)

        gx = correlate1d(
            correlate1d(img, derivada, axis=1, mode="mirror"),
            suavizado,
            axis=0,
            mode="mirror"
        )

        gy = correlate1d(
            correlate1d(img, derivada, axis=0, mode="mirror"),
            suavizado,
            axis=1,
            mode="mirror"
        )

        magnitud = np.hypot(gx, gy)

        if magnitud.max() > 0:
            magnitud = magnitud / magnitud.max() * 255.0

        return np.clip(
            magnitud,
            0,
            255
        ).astype(np.uint8)

    return IM.copy()


# ============================================================
# CONFIGURACIÓN DE CONTROLES (SLIDERS)
# ============================================================

# Sliders de parámetros. Cada método muestra solo los que necesita.
PARAMETROS_METODO = {
    "brillo": {
        "id": "rx-brillo",
        "titulo": "Brillo",
        "subtitulo": "Luminosidad",
        "min": -255, "max": 255, "step": 1, "value": 0,
        "marks": [-255, 0, 255],
    },
    "contraste": {
        "id": "rx-contraste",
        "titulo": "Contraste",
        "subtitulo": "Ganancia lineal",
        "min": 0.1, "max": 3.0, "step": 0.1, "value": 1.0,
        "marks": [0.1, 1, 2, 3],
    },
    "clip_limit": {
        "id": "rx-clip-limit",
        "titulo": "ClipLimit",
        "subtitulo": "Límite de contraste",
        "min": 0.5, "max": 10.0, "step": 0.5, "value": 2.0,
        "marks": [0.5, 2, 5, 10],
    },
    "tile_grid": {
        "id": "rx-tile-grid",
        "titulo": "TileGrid",
        "subtitulo": "Regiones por lado",
        "min": 2, "max": 16, "step": 1, "value": 8,
        "marks": [2, 4, 8, 12, 16],
    },
    "gamma": {
        "id": "rx-gamma",
        "titulo": "Gamma",
        "subtitulo": "Intensidad tonal",
        "min": 0.1, "max": 5.0, "step": 0.1, "value": 1.0,
        "marks": [0.1, 1, 2, 3, 4, 5],
    },
}

# Qué sliders se muestran para cada método.
METODOS_SLIDERS = {
    "brillo": ["brillo"],
    "contraste": ["contraste"],
    "brillo_contraste": ["brillo", "contraste"],
    "ghe": [],
    "clahe": ["clip_limit", "tile_grid"],
    "gamma": ["gamma"],
    "filtro": [],
}

# Mensaje para los métodos que no tienen sliders propios.
MENSAJES_SIN_PARAMETROS = {
    "ghe": (
        "La ecualización global (GHE) no requiere parámetros: "
        "redistribuye automáticamente los niveles de gris."
    ),
    "filtro": (
        "En este modo solo se aplica el filtro seleccionado; "
        "ajusta su kernel en la sección «Filtro de imagen»."
    ),
}

# Slider de kernel de cada filtro.
FILTROS_KERNEL = {
    "Gaussiano": {
        "id": "rx-kernel-gaussiano",
        "titulo": "Kernel",
        "subtitulo": "Tamaño de la ventana (impar)",
        "min": 3, "max": 15, "step": 2, "value": 5,
        "marks": [3, 5, 7, 9, 11, 13, 15],
    },
    "Mediana": {
        "id": "rx-kernel-mediana",
        "titulo": "Kernel",
        "subtitulo": "Tamaño de la ventana (impar)",
        "min": 3, "max": 9, "step": 2, "value": 5,
        "marks": [3, 5, 7, 9],
    },
    "Bilateral": {
        "id": "rx-kernel-bilateral",
        "titulo": "Diámetro",
        "subtitulo": "Vecindad de píxeles (impar)",
        "min": 3, "max": 15, "step": 2, "value": 5,
        "marks": [3, 5, 7, 9, 11, 13, 15],
    },
    "Sobel": {
        "id": "rx-kernel-sobel",
        "titulo": "Kernel",
        "subtitulo": "Apertura del operador (impar)",
        "min": 1, "max": 7, "step": 2, "value": 3,
        "marks": [1, 3, 5, 7],
    },
}

METODO_INICIAL = "brillo"
FILTRO_INICIAL = "Ninguno"

VALORES_POR_DEFECTO = {
    "brillo": 0,
    "contraste": 1.0,
    "clip_limit": 2.0,
    "tile_grid": 8,
    "gamma": 1.0,
    "kernel": 5,
}


# ============================================================
# PIPELINE: MÉTODO + FILTRO
# ============================================================

def reunir_parametros(
    brillo,
    contraste,
    clip_limit,
    tile_grid,
    gamma,
    filtro,
    kernels
):
    """
    Agrupa los valores de los sliders en un diccionario.

    kernels: lista con el valor de cada slider de kernel,
    en el orden de FILTROS_KERNEL.
    """

    por_filtro = dict(
        zip(FILTROS_KERNEL.keys(), kernels)
    )

    return {
        "brillo": brillo,
        "contraste": contraste,
        "clip_limit": clip_limit,
        "tile_grid": tile_grid,
        "gamma": gamma,
        "kernel": por_filtro.get(filtro),
    }


def aplicar_pipeline(
    imagen,
    metodo,
    filtro,
    parametros=None
):
    """
    Aplica el método de procesamiento y luego el filtro.

    Devuelve:
        (imagen_procesada, descripcion, nombre_archivo, parametros_usados)
    """

    p = dict(VALORES_POR_DEFECTO)

    p.update(
        {
            k: v
            for k, v in (parametros or {}).items()
            if v is not None
        }
    )

    partes = []
    usados = {}
    base = None

    if metodo == "brillo":

        procesada = ajustar_brillo(imagen, p["brillo"])
        usados["brillo"] = int(p["brillo"])
        partes.append(f"Brillo aplicado: {usados['brillo']}")
        base = f"brillo_{usados['brillo']}"

    elif metodo == "contraste":

        procesada = ajustar_contraste(imagen, p["contraste"])
        usados["contraste"] = round(float(p["contraste"]), 2)
        partes.append(f"Contraste aplicado: {usados['contraste']:.1f}")
        base = f"contraste_{usados['contraste']:.1f}"

    elif metodo == "brillo_contraste":

        procesada = aplicar_brillo_y_contraste(
            imagen,
            p["brillo"],
            p["contraste"]
        )
        usados["brillo"] = int(p["brillo"])
        usados["contraste"] = round(float(p["contraste"]), 2)
        partes.append(
            f"Brillo: {usados['brillo']} | "
            f"Contraste: {usados['contraste']:.1f}"
        )
        base = "brillo_contraste"

    elif metodo == "ghe":

        procesada = ecualizar_histograma(imagen)
        partes.append("Ecualización global del histograma (GHE)")
        base = "GHE"

    elif metodo == "clahe":

        procesada = ecualizar_clahe(
            imagen,
            p["clip_limit"],
            p["tile_grid"]
        )
        usados["clip_limit"] = round(float(p["clip_limit"]), 2)
        usados["tile_grid"] = int(p["tile_grid"])
        partes.append(
            f"CLAHE (ClipLimit={usados['clip_limit']:.1f}, "
            f"TileGrid={usados['tile_grid']}×{usados['tile_grid']})"
        )
        base = (
            f"CLAHE_clip{usados['clip_limit']:.1f}"
            f"_grid{usados['tile_grid']}"
        )

    elif metodo == "gamma":

        procesada = aplicar_gamma(imagen, p["gamma"])
        usados["gamma"] = round(float(p["gamma"]), 2)
        partes.append(f"Corrección gamma: {usados['gamma']:.1f}")
        base = f"gamma_{usados['gamma']:.1f}"

    else:
        # "filtro" u otro valor: solo se aplica el filtro elegido
        procesada = imagen.copy()

    if filtro and filtro != "Ninguno":

        k = normalizar_kernel(filtro, p["kernel"])

        procesada = aplicar_filtro(procesada, filtro, k)

        usados["kernel"] = k

        if filtro == "Bilateral":
            partes.append(f"Filtro Bilateral (diámetro {k})")
        else:
            partes.append(f"Filtro {filtro} (kernel {k}×{k})")

        etiqueta = f"{filtro}_k{k}"

        base = etiqueta if base is None else f"{base}_{etiqueta}"

    if not partes:
        partes.append("Sin procesamiento")

    if base is None:
        base = "procesada"

    descripcion = " + ".join(partes)

    return (
        procesada,
        descripcion,
        f"imagen_{base}.png",
        usados
    )


# ============================================================
# HISTOGRAMA
# ============================================================

def calcular_histograma(IM):
    """
    Calcula el histograma de una imagen en escala de grises.
    """

    if IM is None:
        return np.zeros(
            256,
            dtype=np.int64
        )

    histograma, _ = np.histogram(
        IM.flatten(),
        bins=256,
        range=(0, 256)
    )

    return histograma


# ============================================================
# COMPONENTE DE IMAGEN
# ============================================================

def crear_componente_imagen(IM):

    if IM is None:
        return html.P(
            "No hay imagen disponible.",
            style={
                "color": THEME["text_secondary"],
                "fontSize": "12px",
            }
        )

    imagen = Image.fromarray(
        IM.astype(np.uint8)
    )

    buffer = io.BytesIO()

    imagen.save(
        buffer,
        format="PNG"
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return html.Img(
        src=(
            "data:image/png;base64,"
            + encoded
        ),
        style={
            "maxWidth": "100%",
            "maxHeight": "320px",
            "width": "auto",
            "height": "auto",
            "objectFit": "contain",
            "display": "block",
            "margin": "0 auto",
        }
    )


# ============================================================
# INTERFAZ
# ============================================================


ESTILO_CAJA_VISIBLE = {
    "marginBottom": "22px",
}

ESTILO_OCULTO = {
    "display": "none",
}

ESTILO_MENSAJE = {
    "fontSize": "12px",
    "lineHeight": "1.6",
    "color": THEME["text_secondary"],
    "padding": "14px 16px",
    "border": f"1px dashed {THEME['green_light']}",
    "borderRadius": "12px",
    "backgroundColor": "rgba(255, 251, 247, 0.6)",
}


def _marcas(valores):

    return {
        v: {
            "label": f"{v:g}",
            "style": {
                "color": THEME["text_secondary"]
            },
        }
        for v in valores
    }


def _crear_slider(cfg, visible):
    """
    Slider con encabezado (título + subtítulo). Va dentro de una
    caja cuyo estilo se alterna para mostrarlo u ocultarlo.
    """

    return html.Div(
        [
            html.Div(
                [
                    html.Span(
                        cfg["titulo"],
                        style={
                            "fontSize": "14px",
                            "fontWeight": "700",
                            "color": THEME["text"],
                        },
                    ),
                    html.Span(
                        cfg["subtitulo"],
                        style={
                            "fontSize": "10px",
                            "color": THEME["text_secondary"],
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "7px",
                },
            ),

            dcc.Slider(
                id=cfg["id"],
                min=cfg["min"],
                max=cfg["max"],
                step=cfg["step"],
                value=cfg["value"],
                marks=_marcas(cfg["marks"]),
                tooltip={
                    "placement": "bottom",
                    "always_visible": False,
                },
            ),
        ],
        id=cfg["id"] + "-caja",
        style=(
            ESTILO_CAJA_VISIBLE
            if visible
            else ESTILO_OCULTO
        ),
    )


def crear_card_controles():

    activos = METODOS_SLIDERS[METODO_INICIAL]

    mensaje = MENSAJES_SIN_PARAMETROS.get(METODO_INICIAL)

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "CONTROLES DE PROCESAMIENTO",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "5px",
                        },
                    ),
                    html.Div(
                        "Ajusta los parámetros que modifican la imagen.",
                        style={
                            "fontSize": "12px",
                            "color": THEME["text_secondary"],
                        },
                    ),
                ],
                style={
                    "marginBottom": "19px",
                },
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.Label(
                                "Método de procesamiento",
                                style={
                                    "fontSize": "14px",
                                    "fontWeight": "700",
                                    "color": THEME["text"],
                                    "display": "block",
                                    "marginBottom": "9px",
                                },
                            ),

                            dcc.Dropdown(
                                id="rx-metodo",
                                options=[
                                    {"label": "Brillo", "value": "brillo"},
                                    {"label": "Contraste", "value": "contraste"},
                                    {"label": "Brillo + Contraste", "value": "brillo_contraste"},
                                    {"label": "Ecualización GHE", "value": "ghe"},
                                    {"label": "Ecualización CLAHE", "value": "clahe"},
                                    {"label": "Corrección Gamma", "value": "gamma"},
                                    {"label": "Filtro", "value": "filtro"},
                                ],
                                value=METODO_INICIAL,
                                clearable=False,
                                style={
                                    "color": "#2B3A35",
                                    "fontSize": "13px",
                                },
                            ),

                            html.Div(
                                "Selecciona la técnica que deseas aplicar.",
                                style={
                                    "fontSize": "10px",
                                    "color": THEME["text_secondary"],
                                    "marginTop": "8px",
                                },
                            ),
                        ],
                        style={
                            "flex": "0 0 300px",
                            "minWidth": "260px",
                        },
                    ),

                    # Panel de parámetros: cambia según el método
                    html.Div(
                        [
                            _crear_slider(cfg, clave in activos)
                            for clave, cfg in PARAMETROS_METODO.items()
                        ]
                        + [
                            html.Div(
                                mensaje or "",
                                id="rx-sin-parametros",
                                style=(
                                    ESTILO_MENSAJE
                                    if mensaje
                                    else ESTILO_OCULTO
                                ),
                            )
                        ],
                        id="rx-panel-parametros",
                        style={
                            "flex": "1",
                            "minWidth": "350px",
                            "paddingLeft": "8px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "32px",
                    "flexWrap": "wrap",
                },
            ),
        ],
        style={
            "background": (
                "linear-gradient(135deg, rgb(255, 251, 247) 0%, "
                "rgb(169, 212, 192) 100%)"
            ),
            "border": f"1px solid {THEME['border']}",
            "borderRadius": "16px",
            "padding": "22px 25px 25px 25px",
            "marginBottom": "20px",
            "boxSizing": "border-box",
        },
    )


def crear_card_filtro():

    return html.Div(
        [
            html.Div(
                "FILTRO DE IMAGEN",
                style={
                    "fontSize": "10px",
                    "letterSpacing": "1.8px",
                    "fontWeight": "700",
                    "color": THEME["pink"],
                    "marginBottom": "5px",
                },
            ),

            html.Div(
                "Suaviza o resalta características de la radiografía.",
                style={
                    "fontSize": "12px",
                    "color": THEME["text_secondary"],
                    "marginBottom": "13px",
                },
            ),

            dcc.Dropdown(
                id="rx-filtro",
                options=[
                    {"label": nombre, "value": nombre}
                    for nombre in ["Ninguno"] + list(FILTROS_KERNEL)
                ],
                value=FILTRO_INICIAL,
                clearable=False,
                style={
                    "color": "#2B3A35",
                    "fontSize": "13px",
                },
            ),

            # Slider de kernel: cambia según el filtro
            html.Div(
                [
                    _crear_slider(cfg, nombre == FILTRO_INICIAL)
                    for nombre, cfg in FILTROS_KERNEL.items()
                ]
                + [
                    html.Div(
                        "Selecciona un filtro para ajustar su kernel.",
                        id="rx-kernel-ayuda",
                        style=(
                            {
                                "fontSize": "11px",
                                "color": THEME["text_secondary"],
                            }
                            if FILTRO_INICIAL == "Ninguno"
                            else ESTILO_OCULTO
                        ),
                    )
                ],
                id="rx-panel-kernel",
                style={
                    "marginTop": "18px",
                },
            ),
        ],
        style={
            "backgroundColor": THEME["card"],
            "border": f"1px solid {THEME['border']}",
            "borderRadius": "16px",
            "padding": "20px 25px 22px 25px",
            "marginBottom": "24px",
            "boxSizing": "border-box",
        },
    )



def mostrar_procesamiento():

    return html.Div(
        [
            # ========================================================
            # HERO
            # ========================================================

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "IMAGENOLOGÍA · PROCESAMIENTO",
                                style={
                                    "fontSize": "10px",
                                    "letterSpacing": "2px",
                                    "fontWeight": "700",
                                    "color": THEME["pink"],
                                    "marginBottom": "12px",
                                },
                            ),

                            html.H1(
                                "Procesamiento de imágenes RX",
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
                                "Explora cómo diferentes técnicas de procesamiento "
                                "permiten modificar, resaltar y analizar una "
                                "radiografía digital.",
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
                            "minWidth": "0",
                            "position": "relative",
                            "zIndex": "2",
                        },
                    ),

                    html.Div(
                        [
                            html.Img(
                                src="/assets/interfaz/cientifico.svg", # <-- Tu imagen
                                alt="Icono de Procesamiento",
                                style={
                                    "width": "180px",       # Ajusta el tamaño a tu gusto
                                    "height": "auto",
                                    #"opacity": "0.20",      # Lo mantiene como marca de agua sutil
                                    "marginBottom": "5px",  # Separación con el texto de abajo
                                },
                            ),
                            html.Div(
                                "RX · DIGITAL",
                                style={
                                    "fontSize": "9px",
                                    "letterSpacing": "2px",
                                    "fontWeight": "700",
                                    "color": THEME["green_light"],
                                    "opacity": "0.45",
                                    "marginTop": "-4px",
                                },
                            ),
                        ],
                        style={
                            "width": "180px",
                            "height": "150px",
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
                    "overflow": "hidden",
                },
            ),

            # ========================================================
            # CARGA
            # ========================================================

            html.Div(
                [
                    html.Div(
                        "CARGAR RADIOGRAFÍA",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.8px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "6px",
                        },
                    ),

                    html.P(
                        "Selecciona una imagen para comenzar a experimentar.",
                        style={
                            "fontSize": "12px",
                            "color": THEME["text_secondary"],
                            "margin": "0 0 14px 0",
                        },
                    ),

                    dcc.Upload(
                        id="rx-upload",
                        children=html.Div(
                            [
                                html.Div(
                                    "📁  Seleccionar radiografía",
                                    style={
                                        "fontSize": "17px",
                                        "fontWeight": "700",
                                        "color": THEME["text"],
                                    },
                                ),
                                html.Div(
                                    "PNG · JPG · JPEG · BMP · TIFF",
                                    style={
                                        "fontSize": "11px",
                                        "letterSpacing": "0.4px",
                                        "color": THEME["text_secondary"],
                                        "marginTop": "7px",
                                    },
                                ),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "height": "92px",
                            "borderWidth": "1.5px",
                            "borderStyle": "dashed",
                            "borderColor": THEME["green_light"],
                            "borderRadius": "14px",
                            "textAlign": "center",
                            "backgroundColor": "rgb(252, 244, 235)",
                            "color": THEME["text"],
                            "cursor": "pointer",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "boxSizing": "border-box",
                        },
                        multiple=False,
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "16px",
                    "padding": "20px 24px",
                    "marginBottom": "20px",
                    "boxSizing": "border-box",
                },
            ),

            # ========================================================

            # ========================================================
            # CONTROLES (sliders según el método)
            # ========================================================

            crear_card_controles(),

            # ========================================================
            # FILTRO (kernel según el filtro)
            # ========================================================

            crear_card_filtro(),


            # ========================================================
            # COMPARACIÓN DE IMÁGENES
            # ========================================================

            html.Div(
                [
                    html.Div(
                        "RESULTADO DEL PROCESAMIENTO",
                        style={
                            "display": "inline-block",
                            "padding": "7px 16px",
                            "border": f"1px solid {THEME['green_light']}",
                            "borderRadius": "20px",
                            "color": THEME["green_light"],
                            "fontSize": "12px",
                            "fontWeight": "800",
                            "letterSpacing": "2px",
                            "marginBottom": "12px",
                        },
                    ),

                                        html.H3(
                        [
                            html.I(
                                className="fa-solid fa-x-ray", # <-- Icono de X-Ray
                                style={
                                    "marginRight": "12px",
                                    "color": THEME["pink"], # Le da un toque de color
                                    "fontSize": "26px"      # Un poco más pequeño que el texto
                                }
                            ),
                            "Original vs. Procesada"
                        ],
                        style={
                            "margin": "0 0 22px 0",
                            "fontSize": "30px",
                            "fontWeight": "800",
                            "color": THEME["text"],
                            "letterSpacing": "0.3px",
                            "textAlign": "center",
                            "display": "flex",          # Para alinear el icono con el texto
                            "alignItems": "center",
                            "justifyContent": "center",
                            "gap": "10px",              # Separación entre icono y texto
                        },
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "ORIGINAL",
                                        style={
                                            "fontSize": "10px",
                                            "letterSpacing": "1.5px",
                                            "fontWeight": "700",
                                            "color": THEME["text_secondary"],
                                            "marginBottom": "10px",
                                        },
                                    ),

                                    html.Div(
                                        id="rx-imagen-original",
                                        children=html.Div(
                                            [
                                                html.Div(
                                                    "🩻",
                                                    style={
                                                        "fontSize": "42px",
                                                        "opacity": "0.45",
                                                        "marginBottom": "7px",
                                                    },
                                                ),
                                                html.Div(
                                                    "No se ha cargado ninguna imagen.",
                                                    style={
                                                        "color": THEME[
                                                            "text_secondary"
                                                        ],
                                                        "fontSize": "12px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        style={
                                            "height": "350px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": THEME[
                                                "bg_secondary"
                                            ],
                                            "border": (
                                                f"1px solid "
                                                f"{THEME['border']}"
                                            ),
                                            "borderRadius": "12px",
                                            "padding": "12px",
                                            "boxSizing": "border-box",
                                            "overflow": "hidden",
                                        },
                                    ),
                                ],
                                style={
                                    "flex": "1",
                                    "minWidth": "320px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "PROCESADA",
                                        style={
                                            "fontSize": "10px",
                                            "letterSpacing": "1.5px",
                                            "fontWeight": "700",
                                            "color": THEME["pink"],
                                            "marginBottom": "10px",
                                        },
                                    ),

                                    html.Div(
                                        id="rx-imagen-procesada",
                                        children=html.Div(
                                            [
                                                html.Div(
                                                    "✦",
                                                    style={
                                                        "fontSize": "42px",
                                                        "color": THEME["pink"],
                                                        "opacity": "0.55",
                                                        "marginBottom": "7px",
                                                    },
                                                ),
                                                html.Div(
                                                    "Aquí aparecerá el resultado.",
                                                    style={
                                                        "color": THEME[
                                                            "text_secondary"
                                                        ],
                                                        "fontSize": "12px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        style={
                                            "height": "350px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": THEME[
                                                "bg_secondary"
                                            ],
                                            "border": (
                                                f"1px solid "
                                                f"{THEME['border']}"
                                            ),
                                            "borderRadius": "12px",
                                            "padding": "12px",
                                            "boxSizing": "border-box",
                                            "overflow": "hidden",
                                        },
                                    ),
                                ],
                                style={
                                    "flex": "1",
                                    "minWidth": "320px",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "gap": "20px",
                            "flexWrap": "wrap",
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
                    "padding": "25px 27px 27px 27px",
                    "marginBottom": "24px",
                    "boxSizing": "border-box",
                },
            ),

            # ========================================================
            # HISTOGRAMA
            # ========================================================

            html.Div(
                [
                    html.Div(
                        "ANÁLISIS DE INTENSIDAD",
                        style={
                            "display": "inline-block",
                            "padding": "7px 16px",
                            "border": f"1px solid {THEME['green_light']}",
                            "borderRadius": "20px",
                            "color": THEME["green_light"],
                            "fontSize": "12px",
                            "fontWeight": "800",
                            "letterSpacing": "2px",
                            "marginBottom": "12px",
                        },
                    ),

                                        html.H3(
                        [
                            html.I(
                                className="fa-solid fa-chart-column", # <-- Icono de gráfico de columnas
                                style={
                                    "marginRight": "12px",
                                    "color": THEME["pink"],
                                    "fontSize": "24px"
                                }
                            ),
                            "Comparación de histogramas"
                        ],
                        style={
                            "margin": "0 0 6px 0",
                            "fontSize": "28px",
                            "fontWeight": "800",
                            "color": THEME["text"],
                            "letterSpacing": "0.3px",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "10px",
                        },
                    ),

                    html.P(
                        "Observa cómo cambia la distribución de niveles "
                        "de gris después del procesamiento.",
                        style={
                            "color": THEME["text_secondary"],
                            "fontSize": "12px",
                            "margin": "0 0 16px 0",
                        },
                    ),

                    html.Div(
                        [
                            dcc.Graph(
                                id="rx-histograma",
                                config={
                                    "displayModeBar": False,
                                    "responsive": True,
                                },
                                style={
                                    "width": "100%",
                                    "height": "390px",
                                },
                            )
                        ],
                        style={
                            "width": "100%",
                            "height": "390px",
                            "overflow": "hidden",
                            "borderRadius": "12px",
                            "backgroundColor": THEME["bg_secondary"],
                            "boxSizing": "border-box",
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
                    "padding": "24px 26px 25px 26px",
                    "marginBottom": "24px",
                    "boxSizing": "border-box",
                    "overflow": "hidden",
                },
            ),

            # ========================================================
            # GUARDAR
            # ========================================================

            html.Div(
                [
                    html.Button(
                        "💾  Guardar imagen procesada",
                        id="rx-guardar",
                        n_clicks=0,
                        style={
                            "backgroundColor": THEME["green"],
                            "color": THEME["text"],
                            "border": f"1px solid {THEME['border']}",
                            "borderRadius": "11px",
                            "padding": "12px 24px",
                            "fontSize": "13px",
                            "fontWeight": "700",
                            "cursor": "pointer",
                        },
                    )
                ],
                style={
                    "textAlign": "center",
                    "marginBottom": "5px",
                },
            ),

            html.Div(
                id="rx-info",
                children="Carga una imagen para comenzar.",
                style={
                    "color": THEME["text_secondary"],
                    "textAlign": "center",
                    "fontSize": "12px",
                    "padding": "12px",
                },
            ),

            dcc.Store(
                id="rx-imagen-original-store"
            ),

            dcc.Store(
                id="rx-contexto-gemini"
            ),

            dcc.Download(
                id="rx-download"
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
# CALLBACKS
# ============================================================

def registrar_callbacks(app):

    # ========================================================
    # GUARDAR IMAGEN ORIGINAL EN MEMORIA
    # ========================================================

    @app.callback(

        Output(
            "rx-imagen-original-store",
            "data"
        ),

        Input(
            "rx-upload",
            "contents"
        )

    )
    def guardar_imagen_original(contents):

        if contents is None:
            return None

        return contents


    # ========================================================
    # MOSTRAR IMAGEN ORIGINAL
    # ========================================================

    @app.callback(

        Output(
            "rx-imagen-original",
            "children"
        ),

        Input(
            "rx-imagen-original-store",
            "data"
        )

    )
    def mostrar_original(contents):

        if contents is None:

            return html.P(
                "No se ha cargado ninguna imagen.",
                style={
                    "color": THEME[
                        "text_secondary"
                    ]
                }
            )

        return html.Img(

            src=contents,

            style={
                "maxWidth": "100%",
                "maxHeight": "320px",
                "objectFit": "contain"
            }

        )


    # ========================================================
    # MOSTRAR SOLO LOS SLIDERS DEL MÉTODO SELECCIONADO
    # ========================================================

    @app.callback(
        [
            Output(cfg["id"] + "-caja", "style")
            for cfg in PARAMETROS_METODO.values()
        ]
        + [
            Output("rx-sin-parametros", "style"),
            Output("rx-sin-parametros", "children"),
        ],
        Input("rx-metodo", "value"),
    )
    def actualizar_controles_metodo(metodo):

        activos = METODOS_SLIDERS.get(metodo, [])

        estilos = [
            ESTILO_CAJA_VISIBLE if clave in activos else ESTILO_OCULTO
            for clave in PARAMETROS_METODO
        ]

        mensaje = MENSAJES_SIN_PARAMETROS.get(metodo)

        return estilos + [
            ESTILO_MENSAJE if mensaje else ESTILO_OCULTO,
            mensaje or "",
        ]


    # ========================================================
    # MOSTRAR EL SLIDER DE KERNEL DEL FILTRO SELECCIONADO
    # ========================================================

    @app.callback(
        [
            Output(cfg["id"] + "-caja", "style")
            for cfg in FILTROS_KERNEL.values()
        ]
        + [
            Output("rx-kernel-ayuda", "style"),
        ],
        Input("rx-filtro", "value"),
    )
    def actualizar_controles_filtro(filtro):

        estilos = [
            ESTILO_CAJA_VISIBLE if nombre == filtro else ESTILO_OCULTO
            for nombre in FILTROS_KERNEL
        ]

        ayuda = (
            {
                "fontSize": "11px",
                "color": THEME["text_secondary"],
            }
            if filtro not in FILTROS_KERNEL
            else ESTILO_OCULTO
        )

        return estilos + [ayuda]


    # ========================================================
    # PROCESAR IMAGEN
    # ========================================================

    @app.callback(

        Output(
            "rx-imagen-procesada",
            "children"
        ),

        Output(
            "rx-histograma",
            "figure"
        ),

        Output(
            "rx-info",
            "children"
        ),

        Output(
            "rx-contexto-gemini",
            "data"
        ),

        Input(
            "rx-imagen-original-store",
            "data"
        ),

        Input(
            "rx-metodo",
            "value"
        ),

        Input(
            "rx-brillo",
            "value"
        ),

        Input(
            "rx-contraste",
            "value"
        ),

        Input(
            "rx-clip-limit",
            "value"
        ),

        Input(
            "rx-tile-grid",
            "value"
        ),

        Input(
            "rx-gamma",
            "value"
        ),

        Input(
            "rx-filtro",
            "value"
        ),

        *[
            Input(cfg["id"], "value")
            for cfg in FILTROS_KERNEL.values()
        ]

    )
    def procesar_imagen(
        contents,
        metodo,
        valor_brillo,
        valor_contraste,
        clip_limit,
        tile_grid,
        gamma,
        filtro,
        *kernels
    ):

        if contents is None:

            figura = go.Figure()

            figura.update_layout(
                paper_bgcolor=THEME["bg_secondary"],
                plot_bgcolor=THEME["bg_secondary"],
                font={
                    "family": "'Lora', Georgia, serif",
                    "color": THEME["text"],
                },
                xaxis={
                    "visible": False,
                    "fixedrange": True,
                },
                yaxis={
                    "visible": False,
                    "fixedrange": True,
                },
                margin={
                    "l": 20,
                    "r": 20,
                    "t": 20,
                    "b": 20,
                },
                height=390,
                annotations=[
                    {
                        "text": (
                            "🩻<br><br>"
                            "Carga una radiografía para visualizar "
                            "su distribución de niveles de gris."
                        ),
                        "xref": "paper",
                        "yref": "paper",
                        "x": 0.5,
                        "y": 0.5,
                        "showarrow": False,
                        "align": "center",
                        "font": {
                            "size": 14,
                            "color": THEME["text_secondary"],
                        },
                    }
                ],
            )

            return (
                html.P(
                    "No se ha cargado ninguna imagen.",
                    style={
                        "color": THEME["text_secondary"],
                        "fontSize": "12px",
                    }
                ),
                figura,
                "Carga una imagen para comenzar.",
                None
            )


        imagen = decodificar_imagen(
            contents
        )


        if imagen is None:

            figura = go.Figure()

            figura.update_layout(
                paper_bgcolor=THEME["bg_secondary"],
                plot_bgcolor=THEME["bg_secondary"],
                xaxis={
                    "visible": False,
                    "fixedrange": True,
                },
                yaxis={
                    "visible": False,
                    "fixedrange": True,
                },
                margin={
                    "l": 20,
                    "r": 20,
                    "t": 20,
                    "b": 20,
                },
                height=390,
                annotations=[
                    {
                        "text": (
                            "⚠️<br><br>"
                            "No se pudo leer la imagen cargada."
                        ),
                        "xref": "paper",
                        "yref": "paper",
                        "x": 0.5,
                        "y": 0.5,
                        "showarrow": False,
                        "align": "center",
                        "font": {
                            "size": 14,
                            "color": THEME["text_secondary"],
                        },
                    }
                ],
            )

            return (
                html.P(
                    "No se pudo leer la imagen.",
                    style={
                        "color": THEME["pink_light"],
                        "fontSize": "12px",
                    }
                ),
                figura,
                "Error al leer la imagen.",
                None
            )


        # ====================================================
        # APLICAR MÉTODO + FILTRO (con los parámetros de los sliders)
        # ====================================================

        parametros = reunir_parametros(
            valor_brillo,
            valor_contraste,
            clip_limit,
            tile_grid,
            gamma,
            filtro,
            kernels
        )

        procesada, descripcion, _, parametros_usados = aplicar_pipeline(
            imagen,
            metodo,
            filtro,
            parametros
        )

        # ====================================================
        # HISTOGRAMAS
        # ====================================================

        hist_original = calcular_histograma(
            imagen
        )

        hist_procesada = calcular_histograma(
            procesada
        )


        # ========================================================
        # GRÁFICO DE HISTOGRAMAS
        # ========================================================

        figura = go.Figure()

        # --------------------------------------------------------
        # HISTOGRAMA ORIGINAL
        # --------------------------------------------------------

        figura.add_trace(
            go.Scatter(
                x=list(range(256)),
                y=hist_original,
                mode="lines",
                name="Original",
                line={
                    "color": "#D97D77",
                    "width": 2.5,
                },
                hovertemplate=(
                    "Nivel de gris: %{x}"
                    "<br>Frecuencia: %{y:,}"
                    "<extra>Original</extra>"
                ),
            )
        )

        # --------------------------------------------------------
        # HISTOGRAMA PROCESADO
        # --------------------------------------------------------

        figura.add_trace(
            go.Scatter(
                x=list(range(256)),
                y=hist_procesada,
                mode="lines",
                name="Procesada",
                line={
                    "color": "#E0B96B",
                    "width": 2.5,
                },
                hovertemplate=(
                    "Nivel de gris: %{x}"
                    "<br>Frecuencia: %{y:,}"
                    "<extra>Procesada</extra>"
                ),
            )
        )

        # --------------------------------------------------------
        # DISEÑO DEL GRÁFICO
        # --------------------------------------------------------

        figura.update_layout(
            paper_bgcolor=THEME["bg_secondary"],
            plot_bgcolor=THEME["bg_secondary"],

            font={
                "family": "'Lora', Georgia, serif",
                "color": THEME["text"],
                "size": 12,
            },

            title=None,

            xaxis={
                "title": {
                    "text": "Nivel de gris",
                    "font": {
                        "size": 13,
                        "color": THEME["text"],
                    },
                },
                "range": [0, 255],
                "showgrid": True,
                "gridcolor": "rgba(199, 191, 174, 0.12)",
                "gridwidth": 1,
                "zeroline": False,
                "tickfont": {
                    "size": 11,
                    "color": THEME["text_secondary"],
                },
                "linecolor": "rgba(199, 191, 174, 0.35)",
                "linewidth": 1,
                "fixedrange": True,
            },

            yaxis={
                "title": {
                    "text": "Frecuencia",
                    "font": {
                        "size": 13,
                        "color": THEME["text"],
                    },
                },
                "showgrid": True,
                "gridcolor": "rgba(199, 191, 174, 0.12)",
                "gridwidth": 1,
                "zeroline": False,
                "tickfont": {
                    "size": 11,
                    "color": THEME["text_secondary"],
                },
                "linecolor": "rgba(199, 191, 174, 0.35)",
                "linewidth": 1,
                "fixedrange": True,
            },

            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.01,
                "xanchor": "right",
                "x": 1,
                "font": {
                    "size": 12,
                    "color": THEME["text"],
                },
                "bgcolor": "rgba(0,0,0,0)",
            },

            hoverlabel={
                "bgcolor": THEME["bg"],
                "bordercolor": THEME["border"],
                "font": {
                    "color": THEME["text"],
                    "size": 12,
                },
            },

            margin={
                "l": 65,
                "r": 25,
                "t": 35,
                "b": 60,
            },

            height=390,
            showlegend=True,
        )


        # ====================================================
        # IMAGEN PROCESADA
        # ====================================================

        imagen_component = crear_componente_imagen(
            procesada
        )

        # ====================================================
        # DATOS DEL PROCESAMIENTO PARA GEMINI
        # ====================================================

        contexto_gemini = {
            "metodo": metodo,
            "descripcion": descripcion,
            "parametros": parametros_usados,
            "filtro": filtro,

            "estadisticas_original": {
                "minimo": int(np.min(imagen)),
                "maximo": int(np.max(imagen)),
                "media": float(np.mean(imagen)),
                "mediana": float(np.median(imagen)),
                "desviacion_estandar": float(np.std(imagen)),
            },

            "estadisticas_procesada": {
                "minimo": int(np.min(procesada)),
                "maximo": int(np.max(procesada)),
                "media": float(np.mean(procesada)),
                "mediana": float(np.median(procesada)),
                "desviacion_estandar": float(np.std(procesada)),
            },

            "histograma_original": hist_original.tolist(),
            "histograma_procesada": hist_procesada.tolist(),
        }


        return (

            imagen_component,

            figura,

            descripcion,

            contexto_gemini

        )

    # ========================================================
    # GUARDAR / DESCARGAR IMAGEN PROCESADA
    # ========================================================

    @app.callback(

        Output(
            "rx-download",
            "data"
        ),

        Input(
            "rx-guardar",
            "n_clicks"
        ),

        State(
            "rx-imagen-original-store",
            "data"
        ),

        State(
            "rx-metodo",
            "value"
        ),

        State(
            "rx-brillo",
            "value"
        ),

        State(
            "rx-contraste",
            "value"
        ),

        State(
            "rx-clip-limit",
            "value"
        ),

        State(
            "rx-tile-grid",
            "value"
        ),

        State(
            "rx-gamma",
            "value"
        ),

        State(
            "rx-filtro",
            "value"
        ),

        *[
            State(cfg["id"], "value")
            for cfg in FILTROS_KERNEL.values()
        ],

        prevent_initial_call=True

    )
    def guardar_imagen(
        n_clicks,
        contents,
        metodo,
        valor_brillo,
        valor_contraste,
        clip_limit,
        tile_grid,
        gamma,
        filtro,
        *kernels
    ):

        if not n_clicks:
            return None

        if contents is None:
            return None

        imagen = decodificar_imagen(
            contents
        )

        if imagen is None:
            return None

        # ====================================================
        # RECREAR EL MISMO PROCESAMIENTO MOSTRADO
        # ====================================================

        parametros = reunir_parametros(
            valor_brillo,
            valor_contraste,
            clip_limit,
            tile_grid,
            gamma,
            filtro,
            kernels
        )

        procesada, _, nombre, _ = aplicar_pipeline(
            imagen,
            metodo,
            filtro,
            parametros
        )

        # ====================================================
        # CONVERTIR A PNG
        # ====================================================

        buffer = io.BytesIO()

        Image.fromarray(
            procesada.astype(np.uint8)
        ).save(
            buffer,
            format="PNG"
        )

        buffer.seek(0)

        # ====================================================
        # GUARDAR FÍSICAMENTE EN EL PROYECTO
        # ====================================================

        carpeta_procesadas = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            ),
            "imagenes_rx",
            "procesadas"
        )

        os.makedirs(
            carpeta_procesadas,
            exist_ok=True
        )

        ruta_guardado = os.path.join(
            carpeta_procesadas,
            nombre
        )

        with open(
            ruta_guardado,
            "wb"
        ) as archivo:

            archivo.write(
                buffer.getvalue()
            )

        # ====================================================
        # DESCARGAR TAMBIÉN LA IMAGEN
        # ====================================================

        return dcc.send_bytes(
            buffer.getvalue(),
            nombre
        )
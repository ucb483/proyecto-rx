# ============================================================
# PLATAFORMA EDUCATIVA INTERACTIVA DE RAYOS X
# INTERFAZ PRINCIPAL
# Integrante 1 - Arquitectura + Interfaz
# ============================================================

from dash import dcc, html, Input, Output, State, no_update
import base64

from modulos.teoria_rx import mostrar_teoria
from modulos.formacion_imagen import mostrar_formacion
from modulos.procesamiento import mostrar_procesamiento
from modulos.analisis import mostrar_analisis
from modulos.gemini_rx import (
    mostrar_gemini,
    generar_respuesta_rapida
)

from modulos.imagenes_rx import generar_imagen_rx
from modulos.videos_rx import generar_videos_rx
from modulos.visuales_rx import generar_visual_rx
from modulos.actividades import mostrar_actividades

# ============================================================
# PALETA DE COLORES
# ============================================================

# ============================================================
# PALETA DE COLORES
# ============================================================

THEME = {
    "bg": "#F1F7F3",
    "bg_secondary": "#FFFFFF",
    "card": "#FFFFFF",
    "green": "#A9D4C0",
    "green_light": "#5E8776",
    "pink": "#5E8776",
    "pink_light": "#2B3A35",
    "mauve": "#A9D4C0",
    "text": "#2B3A35",
    "text_secondary": "#5E8776",
    "sidebar_text": "#2B3A35",
    "sidebar_muted": "#5E8776",
    "card_text": "#2B3A35",
    "card_text_secondary": "#5E8776",
    "border": "#5E8776",
}

# ============================================================
# DETECTOR DE TIPO DE CONSULTA IA
# ============================================================

def detectar_tipo_consulta(pregunta):

    texto = pregunta.lower()


    # Primero detectar visuales educativos
    palabras_visual = [
        "cuadro",
        "tabla",
        "comparación",
        "comparacion",
        "comparar",
        "mapa conceptual",
        "mapa mental",
        "diagrama",
        "esquema"
    ]


    if any(p in texto for p in palabras_visual):
        return "visual"



    # Después imágenes médicas
    palabras_imagen = [
        "muéstrame",
        "muestrame",
        "radiografía",
        "radiografia",
        "foto",
        "imagen rx",
        "imagen radiográfica",
        "imagen radiografica"
    ]


    if any(p in texto for p in palabras_imagen):
        return "imagen"



    # Videos
    palabras_video = [
        "video",
        "vídeo",
        "youtube",
        "tutorial",
        "demostración",
        "demostracion"
    ]


    if any(p in texto for p in palabras_video):
        return "video"



    return "gemini"

# ============================================================
# ESTILOS
# ============================================================

STYLE_CONTAINER = {
    "backgroundColor": THEME["bg"],
    "minHeight": "100vh",
    "fontFamily": "'Lora', Georgia, serif",
    "color": THEME["text"],
}


STYLE_SIDEBAR = {
    "position": "fixed",
    "left": "0",
    "top": "0",
    "bottom": "0",
    "width": "255px",
    "padding": "28px 18px",
    "backgroundColor": "rgb(255 249 243)",
    "borderRight": f"1px solid {THEME['green']}",
    "boxSizing": "border-box",
    "overflowY": "auto",
    "boxShadow": "4px 0 24px rgba(94, 135, 118, 0.10)",
}


STYLE_CONTENT = {
    "marginLeft": "255px",
    "padding": "38px 44px 60px 44px",
    "minHeight": "100vh",
    "boxSizing": "border-box",
    "maxWidth": "1400px",
}


# ============================================================
# LOGOTIPO
# ============================================================

def crear_logo():
    return html.Div(
        [
            html.Div(
                [
                    # REEMPLAZAMOS EL EMOJI POR LA IMAGEN SVG
                    html.Img(
                        src="/assets/interfaz/logo_rx.svg", # Ruta de tu SVG
                        alt="Logo Rayos X",
                        style={
                            "width": "38px",       # Ajusta el tamaño a tu gusto
                            "height": "38px",
                            "marginRight": "12px", # Espacio entre el logo y el texto
                            "objectFit": "contain"
                        }
                    ),
                    html.Span(
                        "RAYOS X",
                        style={
                            "fontSize": "25px",
                            "fontWeight": "700",
                            "letterSpacing": "1.5px",
                            "color": THEME["text"],
                        },
                    ),
                ],
                style={"display": "flex", "alignItems": "center"},
            ),
            html.Div(
                "LIBRO ELECTRÓNICO INTERACTIVO",
                style={
                    "fontSize": "9px",
                    "letterSpacing": "1.4px",
                    "color": THEME["pink"],
                    "marginTop": "8px",
                    "fontWeight": "700",
                    "lineHeight": "1.5",
                },
            ),
            html.Div(
                style={
                    "height": "1px",
                    "backgroundColor": THEME["green"],
                    "marginTop": "22px",
                    "marginBottom": "25px",
                }
            ),
        ]
    )

# ============================================================
# ELEMENTO DEL MENÚ
# ============================================================

def crear_item_menu(icono, texto, ruta):

    return dcc.Link(
        html.Div(
            [
                # CAMBIO: Ahora usamos html.I y le pasamos las clases de Font Awesome + tu clase menu-icono
                html.I(
                    className=f"{icono} menu-icono",
                ),

                html.Span(
                    texto,
                    className="menu-texto",
                ),
            ],
            className="menu-item",
        ),
        href=ruta,
        style={
            "textDecoration": "none",
            "color": "inherit",
            "display": "block",
        },
    )

def crear_menu():
    return html.Div(
        [
            html.Div(
                "CONTENIDO",
                style={
                    "fontSize": "9px",
                    "letterSpacing": "1.7px",
                    "color": THEME["pink"],
                    "marginBottom": "12px",
                    "paddingLeft": "13px",
                    "fontWeight": "700",
                },
            ),
            # REEMPLAZAMOS LOS SÍMBOLOS POR ÍCONOS DE FONT AWESOME
            crear_item_menu("fa-solid fa-house", "Inicio", "/"),
            crear_item_menu("fa-solid fa-radiation", "Fundamentos de RX", "/fundamentos"),
            crear_item_menu("fa-solid fa-image", "Formación de imagen", "/formacion"),
            crear_item_menu("fa-solid fa-sliders", "Procesamiento", "/procesamiento"),
            crear_item_menu("fa-solid fa-chart-line", "Análisis", "/analisis"),
            crear_item_menu("fa-solid fa-clipboard-check", "Actividades", "/actividades"),
        ]
    )

def crear_sidebar():
    return html.Div(
        [
            crear_logo(),
            crear_menu(),
            html.Div(
                [
                    html.Div("ÁREA DE APRENDIZAJE", style={
                        "fontSize": "9px",
                        "letterSpacing": "1.3px",
                        "color": THEME["sidebar_muted"],
                        "marginBottom": "6px",
                    }),
                    html.Div("Radiología · Imagenología", style={
                        "fontSize": "12px",
                        "fontWeight": "700",
                        "color": THEME["pink"],
                    }),
                    html.Div("Plataforma interactiva de Rayos X", style={
                        "fontSize": "10px",
                        "color": THEME["sidebar_muted"],
                        "marginTop": "4px",
                        "lineHeight": "1.4",
                    }),
                ],
                style={
                    "position": "absolute",
                    "left": "15px",
                    "right": "15px",
                    "bottom": "28px",
                    "borderTop": f"1px solid {THEME['green']}",
                    "paddingTop": "18px",
                },
            ),
        ],
        style=STYLE_SIDEBAR,
    )

def crear_etiqueta(texto):
    return html.Div(
        texto.upper(),
        style={
            "fontSize": "10px",
            "letterSpacing": "2px",
            "color": THEME["pink"],
            "fontWeight": "700",
            "marginBottom": "14px",
        },
    )

def crear_tarjeta(icono, titulo, descripcion, ruta):
    return html.Div(
        [
            html.Div(
                [
                    html.I(
                        className=icono,
                        style={
                            "fontSize": "22px",
                            "marginRight": "12px",
                            "color": THEME["pink"], # Mantiene tu paleta
                            "width": "24px", # Para que los iconos queden alineados
                            "textAlign": "center"
                        }
                    ),
                    html.Span(titulo, style={
                        "fontSize": "18px",
                        "fontWeight": "700",
                        "color": THEME["card_text"],
                    }),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "18px",
                },
            ),

            html.P(
                descripcion,
                style={
                    "fontSize": "13px",
                    "lineHeight": "1.65",
                    "color": THEME["card_text_secondary"],
                    "margin": "0 0 20px 0",
                    "textAlign": "justify",
                },
            ),

            dcc.Link(
                "Explorar →",
                href=ruta,
                className="explorar-link",
            ),
        ],
        className="home-card",
        style={
            "backgroundColor": "rgb(255 251 247)",
            "border": f"3px solid {THEME['border']}",
            "borderRadius": "14px",
            "padding": "26px 28px",
            "minHeight": "190px",
            "boxSizing": "border-box",
            "boxShadow": "0 6px 18px rgba(94, 135, 118, 0.14)",
        },
    )

def crear_indicador(numero, titulo):
    return html.Div(
        [
            html.Div(numero, style={
                "fontSize": "25px",
                "fontWeight": "700",
                "color": THEME["text"],
            }),
            html.Div(titulo, style={
                "fontSize": "10px",
                "color": THEME["sidebar_muted"],
                "marginTop": "4px",
            }),
        ],
        className="stat-card",
        style={
            "backgroundColor": THEME["bg_secondary"],
            "border": f"1px solid {THEME['green']}",
            "borderRadius": "10px",
            "padding": "13px 18px",
            "minWidth": "110px",
            "boxShadow": "0 3px 10px rgba(94, 135, 118, 0.10)",
        },
    )

def crear_inicio():
    return html.Div(
        [
            # ============================================================
            # HERO PRINCIPAL
            # ============================================================

            crear_etiqueta("Radiología · Imagenología"),
            html.H1(
                [
                    "Plataforma Educativa de ",
                    html.Span("Rayos X", style={"color": THEME["pink"]}),
                ],
                style={
                    "fontSize": "44px",
                    "fontWeight": "700",
                    "lineHeight": "1.15",
                    "letterSpacing": "-1px",
                    "margin": "0 0 14px 0",
                    "color": THEME["text"],
                },
            ),
            html.P(
                "Explora la física detrás de los Rayos X, la formación de imágenes, "
                "el procesamiento digital, el análisis radiográfico y un asistente de "
                "IA especializado — todo en un solo recorrido interactivo.",
                style={
                    "fontSize": "15px",
                    "lineHeight": "1.7",
                    "maxWidth": "820px",
                    "color": THEME["text_secondary"],
                    "margin": "0 0 28px 0",
                    "textAlign": "justify",
                },
            ),
            html.Div(
                style={
                    "width": "65px",
                    "height": "3px",
                    "backgroundColor": THEME["pink"],
                    "marginBottom": "32px",
                }
            ),
            dcc.Link(
                html.Button(
                    "COMENZAR RECORRIDO  →",
                    style={
                        "backgroundColor": THEME["pink"],
                        "color": THEME["bg"],
                        "border": "none",
                        "borderRadius": "7px",
                        "padding": "12px 22px",
                        "fontSize": "11px",
                        "fontWeight": "700",
                        "letterSpacing": "0.8px",
                        "cursor": "pointer",
                        "marginBottom": "35px",
                    },
                ),
                href="/fundamentos",
                style={"textDecoration": "none"},
            ),

            # ============================================================
            # GRILLA DE MÓDULOS · ELEMENTO PRINCIPAL DE LA PORTADA
            # ============================================================

            html.Div(
                [
                    html.H2("Comienza tu recorrido", style={
                        "fontSize": "23px",
                        "fontWeight": "700",
                        "margin": "0 0 7px 0",
                        "color": THEME["text"],
                    }),
                    html.P("Explora la plataforma paso a paso.", style={
                        "fontSize": "12px",
                        "color": THEME["text_secondary"],
                        "margin": "0 0 22px 0",
                    }),
                    html.Div(
    [
        crear_tarjeta(
            "fa-solid fa-radiation",
            "Fundamentos de RX",
            "Comprende la naturaleza de los Rayos X, sus propiedades y los principios físicos que permiten su utilización.",
            "/fundamentos",
        ),
        crear_tarjeta(
            "fa-solid fa-bolt",
            "Producción de RX",
            "Conoce el funcionamiento del tubo de Rayos X, el cátodo, el ánodo y la producción de radiación.",
            "/produccion",
        ),
        crear_tarjeta(
            "fa-solid fa-image",
            "Formación de imagen",
            "Explora la atenuación, las interacciones con la materia y el proceso de formación de una imagen radiográfica.",
            "/formacion",
        ),
        crear_tarjeta(
            "fa-solid fa-sliders",
            "Procesamiento",
            "Trabaja con imágenes radiográficas y comprende diferentes técnicas de procesamiento digital.",
            "/procesamiento",
        ),
        crear_tarjeta(
            "fa-solid fa-chart-line",
            "Análisis",
            "Obtén información cuantitativa de las imágenes y compara diferentes resultados.",
            "/analisis",
        ),
    ],
    style={
        "display": "grid",
        "gridTemplateColumns": "repeat(2, minmax(280px, 1fr))",
        "gap": "18px",
        "maxWidth": "1100px",
    },
),
                ]
            ),

            # ============================================================
            # UN POCO DE HISTORIA (CIERRE DE LA PORTADA)
            # ============================================================

            html.Div(
                [
                    html.Br(),
                    html.Div(
                        "UN POCO DE HISTORIA",
                        style={
                            "fontSize": "18px",
                            "letterSpacing": "2px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "10px",
                        },
                    ),
                    html.H2(
                        "De Röntgen a Curie: los orígenes de los Rayos X",
                        style={
                            "fontSize": "23px",
                            "fontWeight": "700",
                            "margin": "0 0 7px 0",
                            "color": THEME["text"],
                        },
                    ),
                    html.P(
                        "Conoce a las personas y los hechos que dieron origen a la radiología.",
                        style={
                            "fontSize": "12px",
                            "color": THEME["text_secondary"],
                            "margin": "0 0 22px 0",
                        },
                    ),
                ]
            ),

            html.Div(
                [
                    # --------------------------------------------------------
                    # COLUMNA PRINCIPAL: INTRODUCCIÓN
                    # --------------------------------------------------------

                    html.Div(
                        [
                            html.Div(
                                "BIENVENIDO AL MUNDO DE LOS RAYOS X",
                                style={
                                    "fontSize": "10px",
                                    "letterSpacing": "2px",
                                    "fontWeight": "700",
                                    "color": THEME["pink"],
                                    "marginBottom": "12px",
                                },
                            ),

                            html.H2(
                                "Una ventana al interior del cuerpo humano",
                                style={
                                    "fontSize": "29px",
                                    "fontWeight": "700",
                                    "lineHeight": "1.25",
                                    "color": THEME["text"],
                                    "margin": "0 0 15px 0",
                                },
                            ),

                            html.P(
                                "Los Rayos X revolucionaron la medicina al permitir "
                                "observar el interior del cuerpo humano sin necesidad "
                                "de realizar una cirugía. En esta plataforma podrás "
                                "seguir el recorrido completo: desde la producción "
                                "de los Rayos X hasta la formación, procesamiento "
                                "y análisis de una imagen radiográfica.",
                                style={
                                    "fontSize": "14px",
                                    "lineHeight": "1.8",
                                    "color": THEME["card_text_secondary"],
                                    "maxWidth": "600px",
                                    "textAlign": "justify",
                                    "margin": "0 0 22px 0",
                                },
                            ),

                            # ------------------------------------------------
                            # LÍNEA HISTÓRICA
                            # ------------------------------------------------

                            html.Div(
                                [
                                    html.Div(
                                        "1895",
                                        style={
                                            "fontSize": "24px",
                                            "fontWeight": "700",
                                            "color": THEME["pink"],
                                            "minWidth": "65px",
                                        },
                                    ),

                                    html.Div(
                                        [
                                            html.Div(
                                                "Descubrimiento de los Rayos X",
                                                style={
                                                    "fontSize": "13px",
                                                    "fontWeight": "700",
                                                    "color": THEME["text"],
                                                    "marginBottom": "4px",
                                                },
                                            ),

                                            html.Div(
                                                "Wilhelm Conrad Röntgen identifica "
                                                "una nueva forma de radiación.",
                                                style={
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                    "color": THEME[
                                                        "card_text_secondary"
                                                    ],
                                                },
                                            ),
                                        ],
                                        style={
                                            "borderLeft": (
                                                f"2px solid "
                                                f"{THEME['pink']}"
                                            ),
                                            "paddingLeft": "16px",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "12px",
                                    "marginBottom": "24px",
                                },
                            ),

                            # ------------------------------------------------
                            # DATOS CURIOSOS
                            # ------------------------------------------------

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                "01",
                                                style={
                                                    "fontSize": "10px",
                                                    "fontWeight": "700",
                                                    "color": THEME["pink"],
                                                    "marginBottom": "5px",
                                                },
                                            ),

                                            html.Div(
                                                "La primera radiografía médica "
                                                "fue realizada sobre una mano.",
                                                style={
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                    "color": THEME[
                                                        "card_text_secondary"
                                                    ],
                                                },
                                            ),
                                        ],
                                        style={
                                            "flex": "1",
                                            "padding": "12px 14px",
                                            "border": (
                                                f"2px solid "
                                                f"{THEME['green']}"
                                            ),
                                            "borderRadius": "9px",
                                            "backgroundColor": "rgb(252 244 235)",
                                        },
                                    ),

                                    html.Div(
                                        [
                                            html.Div(
                                                "02",
                                                style={
                                                    "fontSize": "10px",
                                                    "fontWeight": "700",
                                                    "color": THEME["pink"],
                                                    "marginBottom": "5px",
                                                },
                                            ),

                                            html.Div(
                                                "Los Rayos X son radiación "
                                                "electromagnética ionizante.",
                                                style={
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                    "color": THEME[
                                                        "card_text_secondary"
                                                    ],
                                                },
                                            ),
                                        ],
                                        style={
                                            "flex": "1",
                                            "padding": "12px 14px",
                                            "border": (
                                                f"2px solid "
                                                f"{THEME['green']}"
                                            ),
                                            "borderRadius": "9px",
                                            "backgroundColor": "rgb(252 244 235)",
                                        },
                                    ),

                                    html.Div(
                                        [
                                            html.Div(
                                                "03",
                                                style={
                                                    "fontSize": "10px",
                                                    "fontWeight": "700",
                                                    "color": THEME["pink"],
                                                    "marginBottom": "5px",
                                                },
                                            ),

                                            html.Div(
                                                "Una radiografía puede revelar "
                                                "estructuras que no son visibles "
                                                "a simple vista.",
                                                style={
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                    "color": THEME[
                                                        "card_text_secondary"
                                                    ],
                                                },
                                            ),
                                        ],
                                        style={
                                            "flex": "1",
                                            "padding": "12px 14px",
                                            "border": (
                                                f"2px solid "
                                                f"{THEME['green']}"
                                            ),
                                            "borderRadius": "9px",
                                            "backgroundColor": "rgb(252 244 235)",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "gap": "12px",
                                    "maxWidth": "610px",
                                    "flexWrap": "wrap",
                                },
                            ),
                        ],
                        style={
                            "flex": "1.35",
                            "minWidth": "350px",
                        },
                    ),

                    # --------------------------------------------------------
                    # COLUMNA VISUAL: ESPACIO PARA IMAGEN HISTÓRICA
                    # --------------------------------------------------------

                    html.Div(
                        [
                            html.Div(
                                "UN POCO DE HISTORIA",
                                style={
                                    "fontSize": "9px",
                                    "letterSpacing": "1.8px",
                                    "fontWeight": "700",
                                    "color": THEME["pink"],
                                    "marginBottom": "12px",
                                    "textAlign": "center",
                                },
                            ),

                            html.Div(
                                [
                                    html.Img(
                                        src="/assets/interfaz/primera_radiografia.jpg",
                                        alt="Primera radiografía médica histórica",
                                        style={
                                            "width": "100%",
                                            "maxWidth": "245px",
                                            "height": "145px",
                                            "objectFit": "contain",
                                            "borderRadius": "8px",
                                            "display": "block",
                                            "marginBottom": "12px",
                                        },
                                    ),

                                    html.Div(
                                        "La primera radiografía",
                                        style={
                                            "fontSize": "15px",
                                            "fontWeight": "700",
                                            "color": THEME["text"],
                                            "textAlign": "center",
                                        },
                                    ),

                                    html.Div(
                                        "La famosa radiografía de la mano "
                                        "realizada en los primeros días del "
                                        "descubrimiento de los Rayos X.",
                                        style={
                                            "fontSize": "11px",
                                            "lineHeight": "1.5",
                                            "color": THEME[
                                                "card_text_secondary"
                                            ],
                                            "textAlign": "center",
                                            "maxWidth": "245px",
                                            "marginTop": "7px",
                                        },
                                    ),
                                ],
                                style={
                                    "minHeight": "220px",
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "background": "linear-gradient(145deg, rgb(255, 255, 255) 0%, rgb(229 220 205) 100%)",
                                    "border": (
                                        f"3px dashed "
                                        f"{THEME['border']}"
                                    ),
                                    "borderRadius": "12px",
                                    "padding": "20px",
                                    "boxSizing": "border-box",
                                },
                            ),

                            html.Div(
                                "Una ventana al interior del cuerpo humano.",
                                style={
                                    "fontSize": "10px",
                                    "fontStyle": "italic",
                                    "color": THEME["card_text_secondary"],
                                    "textAlign": "center",
                                    "marginTop": "10px",
                                },
                            ),
                        ],
                        style={
                            "flex": "0.8",
                            "minWidth": "260px",
                            "maxWidth": "330px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "42px",
                    "backgroundColor": "rgb(255, 251, 247)",
                    "border": (
                        f"3px solid "
                        f"{THEME['border']}"
                    ),
                    "borderRadius": "16px",
                    "padding": "32px 34px",
                    "maxWidth": "1100px",
                    "boxSizing": "border-box",
                    "marginBottom": "42px",
                },
            ),

            # ============================================================
            # MARIE CURIE · HISTORIA DE LA CIENCIA
            # ============================================================

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "PERSONAJES QUE TRANSFORMARON LA CIENCIA",
                                style={
                                    "fontSize": "9px",
                                    "letterSpacing": "1.8px",
                                    "fontWeight": "700",
                                    "color": THEME["pink"],
                                    "marginBottom": "8px",
                                },
                            ),

                            html.H3(
                                "Marie Curie",
                                style={
                                    "fontSize": "23px",
                                    "fontWeight": "700",
                                    "color": THEME["text"],
                                    "margin": "0 0 8px 0",
                                },
                            ),

                            html.P(
                                "Marie Curie fue una figura fundamental en el "
                                "estudio de la radiactividad y recibió el Premio "
                                "Nobel de Física en 1903. Su trabajo pertenece a "
                                "la historia de la radiación y ayuda a comprender "
                                "el contexto científico en el que se desarrolló "
                                "la radiología.",
                                style={
                                    "fontSize": "12px",
                                    "lineHeight": "1.7",
                                    "color": THEME["card_text_secondary"],
                                    "maxWidth": "620px",
                                    "textAlign": "justify",
                                    "margin": "0",
                                },
                            ),
                        ],
                        style={
                            "flex": "1",
                            "minWidth": "300px",
                        },
                    ),

                    html.Div(
                        [
                            html.Img(
                                src="/assets/interfaz/marie_curie.jpg",
                                alt="Marie Curie",
                                style={
                                    "width": "150px",
                                    "height": "150px",
                                    "objectFit": "cover",
                                    "borderRadius": "10px",
                                    "display": "block",
                                },
                            ),
                        ],
                        style={
                            "flexShrink": "0",
                            "padding": "5px",
                            "border": (
                                f"3px solid "
                                f"{THEME['border']}"
                            ),
                            "borderRadius": "12px",
                            "backgroundColor": THEME["bg_secondary"],
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "space-between",
                    "gap": "28px",
                    "backgroundColor": "rgb(255, 251, 247)",
                    "border": (
                        f"3px solid "
                        f"{THEME['border']}"
                    ),
                    "borderRadius": "14px",
                    "padding": "22px 26px",
                    "maxWidth": "1100px",
                    "boxSizing": "border-box",
                    "marginBottom": "42px",
                },
            ),
        ]
    )


def crear_pagina_provisional(titulo, descripcion, responsable):

    return html.Div(
        [

            crear_etiqueta("Módulo educativo"),

            html.H1(
                titulo,
                style={
                    "fontSize": "38px",
                    "fontWeight": "500",
                    "color": THEME["text"],
                    "marginBottom": "15px",
                },
            ),

            html.P(
                descripcion,
                style={
                    "fontSize": "15px",
                    "lineHeight": "1.7",
                    "color": THEME["text_secondary"],
                    "maxWidth": "700px",
                    "marginBottom": "30px",
                    "textAlign": "justify",
                },
            ),

            html.Div(
                [
                    html.Div(
                        "MÓDULO EN PREPARACIÓN",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.5px",
                            "color": THEME["pink_light"],
                            "fontWeight": "700",
                            "marginBottom": "10px",
                        },
                    ),

                    html.Div(
                        responsable,
                        style={
                            "fontSize": "13px",
                            "color": THEME["text_secondary"],
                        },
                    ),
                ],
                style={
                    "backgroundColor": THEME["card"],
                    "border": f"1px solid {THEME['border']}",
                    "borderLeft": f"3px solid {THEME['pink']}",
                    "borderRadius": "10px",
                    "padding": "22px",
                    "maxWidth": "700px",
                },
            ),

        ]
    )



# ============================================================
# ASISTENTE IA FLOTANTE
# ============================================================

def crear_asistente_flotante():
    return html.Div(
        [
            # Botón flotante
            html.Button(
                [
                    html.Span("✦", style={
                        "fontSize": "18px",
                        "marginRight": "8px",
                    }),
                    "ASISTENTE IA",
                ],
                id="boton-asistente-ia",
                n_clicks=0,
                style={
                    "position": "fixed",
                    "right": "24px",
                    "bottom": "22px",
                    "zIndex": "1001",
                    "backgroundColor": THEME["pink"],
                    "color": THEME["bg_secondary"],
                    "border": f"1px solid {THEME['pink']}",
                    "borderRadius": "24px",
                    "padding": "13px 20px",
                    "fontSize": "11px",
                    "fontWeight": "700",
                    "letterSpacing": "1px",
                    "cursor": "pointer",
                    "boxShadow": "0 8px 24px rgba(0,0,0,0.28)",
                },
            ),

            # Ventana de conversación
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div("✦", style={
                                        "fontSize": "20px",
                                        "color": THEME["pink"],
                                        "marginRight": "10px",
                                    }),
                                    html.Div(
                                        [
                                            html.Div("ASISTENTE IA", style={
                                                "fontSize": "12px",
                                                "fontWeight": "700",
                                                "letterSpacing": "1px",
                                                "color": THEME["text"],
                                            }),
                                            html.Div("Rayos X · Tutor académico", style={
                                                "fontSize": "9px",
                                                "color": THEME["text_secondary"],
                                                "marginTop": "3px",
                                            }),
                                        ]
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "center"},
                            ),
                            html.Button(
                                "×",
                                id="cerrar-asistente-ia",
                                n_clicks=0,
                                style={
                                    "background": "transparent",
                                    "border": "none",
                                    "color": THEME["text_secondary"],
                                    "fontSize": "24px",
                                    "cursor": "pointer",
                                    "lineHeight": "1",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                            "padding": "15px 16px",
                            "borderBottom": f"1px solid {THEME['green']}",
                        },
                    ),

                    html.Div(
                        id="historial-visible-gemini-flotante",
                        children=html.Div(
                            "Hola 👋 Soy tu asistente de IA para Rayos X. ¿Qué quieres aprender?",
                            style={
                                "backgroundColor": THEME["bg"],
                                "color": THEME["text"],
                                "borderRadius": "10px",
                                "padding": "11px 12px",
                                "fontSize": "11px",
                                "lineHeight": "1.5",
                            },
                        ),
                        style={
                            "flex": "1",
                            "overflowY": "auto",
                            "padding": "14px",
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "9px",
                        },
                    ),

                    html.Div(
                        [
                            dcc.Textarea(
                                id="input-pregunta-gemini-flotante",
                                placeholder="Escribe tu pregunta...",
                                style={
                                    "width": "100%",
                                    "height": "58px",
                                    "resize": "none",
                                    "boxSizing": "border-box",
                                    "backgroundColor": THEME["bg"],
                                    "color": THEME["text"],
                                    "border": f"1px solid {THEME['green']}",
                                    "borderRadius": "9px",
                                    "padding": "9px 10px",
                                    "fontSize": "11px",
                                    "fontFamily": "'Lora', Georgia, serif",
                                    "outline": "none",
                                },
                            ),
                            html.Button(
                                "Preguntar →",
                                id="btn-consultar-gemini-flotante",
                                n_clicks=0,
                                style={
                                    "width": "100%",
                                    "marginTop": "8px",
                                    "backgroundColor": THEME["pink"],
                                    "color": THEME["bg_secondary"],
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "padding": "10px",
                                    "fontSize": "10px",
                                    "fontWeight": "700",
                                    "letterSpacing": "0.8px",
                                    "cursor": "pointer",
                                },
                            ),
                        ],
                        style={
                            "padding": "12px 14px 14px 14px",
                            "borderTop": f"1px solid {THEME['green']}",
                        },
                    ),

                    dcc.Store(id="historial-gemini-flotante", data=[]),
                ],
                id="ventana-asistente-ia",
                style={
                    "display": "none",
                    "position": "fixed",
                    "right": "24px",
                    "bottom": "76px",
                    "width": "360px",
                    "height": "470px",
                    "zIndex": "1000",
                    "backgroundColor": THEME["bg_secondary"],
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "15px",
                    "boxShadow": "0 18px 50px rgba(0,0,0,0.38)",
                    "overflow": "hidden",
                    "flexDirection": "column",
                },
            ),
        ]
    )


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

def crear_layout():

    return html.Div(
        [

            dcc.Location(
                id="url",
                refresh=False,
            ),

            dcc.Store(
                id="rx-contexto-gemini",
                data=None,
            ),

            dcc.Store(
                id="rx-histograma-contexto",
                data=None,
            ),
            crear_sidebar(),

            html.Main(
                id="contenido-principal",
                children=crear_inicio(),
                style=STYLE_CONTENT,
            ),

            html.Div(
                id="asistente-flotante-contenedor",
                children=crear_asistente_flotante(),
            ),

        ],
        style=STYLE_CONTAINER,
    )
# ============================================================
# NAVEGACIÓN ENTRE SECCIONES
# ============================================================


# ============================================================
# RENDERIZAR RESPUESTAS DEL ASISTENTE (TEXTO + IMÁGENES)
# ============================================================

def renderizar_respuesta(respuesta):

    if isinstance(respuesta, dict):

        if respuesta.get("tipo") == "imagen":

            return html.Img(
                src=respuesta.get("contenido"),
                style={
                    "width": "100%",
                    "maxWidth": "700px",
                    "borderRadius": "10px",
                    "marginTop": "10px"
                }
            )

        if respuesta.get("tipo") == "texto":
            return respuesta.get("contenido", "")

    return respuesta



def registrar_callbacks(app):

    @app.callback(
        Output("asistente-flotante-contenedor", "style"),
        Input("url", "pathname"),
    )
    def controlar_asistente(pathname):

        if pathname == "/actividades":
            return {"display": "none"}

        return {"display": "block"}

    @app.callback(
        Output("ventana-asistente-ia", "style"),
        Input("boton-asistente-ia", "n_clicks"),
        Input("cerrar-asistente-ia", "n_clicks"),
        prevent_initial_call=True,
    )
    def alternar_asistente(abrir, cerrar):
        from dash import callback_context

        if not callback_context.triggered:
            return no_update

        disparador = callback_context.triggered[0]["prop_id"].split(".")[0]

        if disparador == "boton-asistente-ia":
            return {
                "display": "flex",
                "position": "fixed",
                "right": "24px",
                "bottom": "76px",
                "width": "360px",
                "height": "470px",
                "zIndex": "1000",
                "backgroundColor": THEME["bg_secondary"],
                "border": f"1px solid {THEME['border']}",
                "borderRadius": "15px",
                "boxShadow": "0 18px 50px rgba(0,0,0,0.38)",
                "overflow": "hidden",
                "flexDirection": "column",
            }

        return {"display": "none"}

    @app.callback(
        Output("historial-visible-gemini-flotante", "children"),
        Output("historial-gemini-flotante", "data"),
        Input("btn-consultar-gemini-flotante", "n_clicks"),
        State("input-pregunta-gemini-flotante", "value"),
        State("historial-gemini-flotante", "data"),
        State("rx-contexto-gemini", "data"),
        prevent_initial_call=True,
    )
    def consultar_asistente_flotante(
        n_clicks,
        pregunta,
        historial,
        contexto_rx
    ):
        if not pregunta or not pregunta.strip():
            return no_update, no_update

        if historial is None:
            historial = []

        pregunta = pregunta.strip()
        tipo = detectar_tipo_consulta(pregunta)

        if tipo == "imagen":
            respuesta = generar_imagen_rx(
                pregunta,
                historial
            )

        elif tipo == "video":
            respuesta = generar_videos_rx(
                pregunta,
                historial
            )

        elif tipo == "visual":

            resultado_visual = generar_visual_rx(
                pregunta,
                historial
            )

            if resultado_visual.get("ok"):

                respuesta = html.Img(
                    src=(
                        "data:image/png;base64,"
                        + resultado_visual["imagen"]
                    ),
                    style={
                        "width": "100%",
                        "maxWidth": "700px",
                        "borderRadius": "10px",
                        "marginTop": "10px"
                    }
                )

            else:

                respuesta = (
                    "Error generando visual: "
                    + resultado_visual.get(
                        "error",
                        "Error desconocido"
                    )
                )

        else:
            respuesta = generar_respuesta_rapida(
                pregunta
            )

        # Guardar respuestas compatibles con dcc.Store
        if isinstance(respuesta, html.Img):

            respuesta_historial = {
                "tipo": "imagen",
                "contenido": respuesta.src
            }

        else:

            respuesta_historial = {
                "tipo": "texto",
                "contenido": str(respuesta)
            }


        nuevo_historial = historial + [{
            "pregunta": pregunta,
            "respuesta": respuesta_historial,
        }]

        mensajes = []

        for mensaje in nuevo_historial:
            mensajes.append(
                html.Div(
                    [
                        html.Div("Tú", style={
                            "fontSize": "9px",
                            "fontWeight": "700",
                            "color": THEME["pink"],
                            "marginBottom": "4px",
                        }),
                        html.Div(mensaje["pregunta"], style={
                            "fontSize": "11px",
                            "lineHeight": "1.45",
                            "color": THEME["text"],
                            "marginBottom": "8px",
                        }),
                        html.Div("ASISTENTE IA", style={
                            "fontSize": "9px",
                            "fontWeight": "700",
                            "color": THEME["green_light"],
                            "marginBottom": "4px",
                        }),
                        html.Div(
                            renderizar_respuesta(
                                mensaje["respuesta"]
                            ),
                            style={
                                "fontSize": "11px",
                                "lineHeight": "1.5",
                                "color": THEME["text"],
                                "whiteSpace": "pre-wrap",
                            }
                        ),
                    ],
                    style={
                        "backgroundColor": THEME["bg"],
                        "borderRadius": "10px",
                        "padding": "10px 11px",
                        "borderLeft": f"3px solid {THEME['pink']}",
                    },
                )
            )

        return mensajes, nuevo_historial

    @app.callback(
        Output("contenido-principal", "children"),
        Input("url", "pathname")
    )
    def cambiar_pagina(pathname):

        if pathname == "/":
            return crear_inicio()

        elif pathname == "/fundamentos":
            return mostrar_teoria()

        elif pathname == "/produccion":
            return mostrar_teoria()

        elif pathname == "/formacion":
            return mostrar_formacion()

        elif pathname == "/detectores":
            return mostrar_formacion()

        elif pathname == "/procesamiento":
            return mostrar_procesamiento()

        elif pathname == "/analisis":
            return mostrar_analisis()

        elif pathname == "/gemini":
            return mostrar_gemini()

        elif pathname == "/actividades":
            return mostrar_actividades()

        else:
            return crear_inicio()
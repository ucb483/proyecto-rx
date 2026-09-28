"""
Módulo de Formación de la Imagen Radiográfica
Proyecto_RX

Función pública:
    mostrar_formacion()

Diseño:
    Mantiene el mismo formato visual utilizado en teoria_rx.py:
    - Hero superior
    - Tarjetas educativas
    - Imágenes dentro de contenedores
    - Pestañas uniformes
    - Flujos horizontales sin desplazamiento
"""

from dash import html, dcc


# ============================================================
# CONFIGURACIÓN
# ============================================================

ASSETS_FORMACION = "/assets/formacion/"

CREMA = "#2B3A35"
BEIGE = "#5E8776"
AZUL_OSCURO = "rgb(252, 244, 235)"
AZUL = "#FFFFFF"
AZUL_MEDIO = "#A9D4C0"
FONDO_CLARO = "rgb(255, 251, 247)"


# ============================================================
# UTILIDADES DE DISEÑO
# ============================================================

def _tarjeta(titulo, contenido, icono="01"):
    """Tarjeta educativa con el mismo estilo general de Teoría."""

    return html.Div(
        [
            html.Div(
                [
                    html.Span(
                        icono,
                        style={
                            "display": "inline-flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "width": "48px",
                            "height": "48px",
                            "minWidth": "48px",
                            "backgroundColor": CREMA,
                            "color": AZUL,
                            "borderRadius": "12px",
                            "fontSize": "14px",
                            "fontWeight": "800",
                            "boxSizing": "border-box",
                        },
                    ),
                    html.H3(
                        titulo,
                        style={
                            "margin": "0",
                            "fontSize": "21px",
                            "lineHeight": "1.2",
                            "fontWeight": "700",
                            "color": CREMA,
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "14px",
                    "marginBottom": "16px",
                },
            ),

            html.Div(
                contenido,
                style={
                    "color": CREMA,
                    "fontSize": "14px",
                    "lineHeight": "1.7",
                },
            ),
        ],
        style={
            "backgroundColor": FONDO_CLARO,
            "border": f"3px solid {AZUL_MEDIO}",
            "borderRadius": "16px",
            "padding": "24px 26px",
            "boxSizing": "border-box",
            "minHeight": "0",
        },
    )


def _imagen(nombre, alt, max_height="330px"):
    """Imagen dentro de un contenedor elegante y adaptable."""

    return html.Div(
        [
            html.Img(
                src=ASSETS_FORMACION + nombre,
                alt=alt,
                style={
                    "display": "block",
                    "width": "100%",
                    "maxWidth": "100%",
                    "height": "auto",
                    "maxHeight": max_height,
                    "objectFit": "contain",
                    "borderRadius": "12px",
                },
            )
        ],
        style={
            "width": "100%",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "overflow": "hidden",
            "backgroundColor": AZUL_OSCURO,
            "border": f"3px solid {AZUL_MEDIO}",
            "borderRadius": "14px",
            "padding": "10px",
            "boxSizing": "border-box",
        },
    )


def _flujo(pasos, altura="76px"):
    """
    Flujo horizontal.
    Todos los pasos permanecen dentro del mismo contenedor:
    no hay barra de desplazamiento horizontal.
    """

    elementos = []

    for i, paso in enumerate(pasos):

        elementos.append(
            html.Div(
                paso,
                style={
                    "flex": "1 1 0",
                    "minWidth": "0",
                    "height": altura,
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": "8px 7px",
                    "boxSizing": "border-box",
                    "backgroundColor": CREMA,
                    "color": AZUL,
                    "border": f"3px solid {BEIGE}",
                    "borderRadius": "12px",
                    "fontFamily": "'Lora', Georgia, serif",
                    "fontSize": "11px",
                    "fontWeight": "700",
                    "lineHeight": "1.2",
                    "textAlign": "center",
                    "whiteSpace": "normal",
                    "overflow": "hidden",
                    "overflowWrap": "break-word",
                },
            )
        )

        if i < len(pasos) - 1:
            elementos.append(
                html.Div(
                    "→",
                    style={
                        "flex": "0 0 24px",
                        "width": "24px",
                        "minWidth": "24px",
                        "height": altura,
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "boxSizing": "border-box",
                        "color": BEIGE,
                        "fontFamily": "'Lora', Georgia, serif",
                        "fontSize": "20px",
                        "fontWeight": "700",
                        "lineHeight": "1",
                    },
                )
            )

    return html.Div(
        elementos,
        style={
            "display": "flex",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "alignItems": "center",
            "width": "100%",
            "minWidth": "0",
            "height": "auto",
            "gap": "5px",
            "padding": "14px 10px",
            "margin": "22px 0 28px 0",
            "boxSizing": "border-box",
            "overflow": "hidden",
            "backgroundColor": FONDO_CLARO,
            "border": f"3px solid {AZUL_MEDIO}",
            "borderRadius": "18px",
        },
    )


def _bloque_explicativo(etiqueta, titulo, texto):
    """Bloque corto para explicar una imagen o concepto."""

    return html.Div(
        [
            html.Div(
                etiqueta,
                style={
                    "fontSize": "10px",
                    "fontWeight": "700",
                    "letterSpacing": "1.4px",
                    "color": BEIGE,
                    "marginBottom": "7px",
                },
            ),
            html.H3(
                titulo,
                style={
                    "margin": "0 0 8px 0",
                    "fontSize": "20px",
                    "lineHeight": "1.25",
                    "color": CREMA,
                },
            ),
            html.P(
                texto,
                style={
                    "margin": "0",
                    "fontSize": "13px",
                    "lineHeight": "1.65",
                    "color": BEIGE,
                },
            ),
        ],
        style={
            "padding": "20px 22px",
            "backgroundColor": FONDO_CLARO,
            "border": f"3px solid {AZUL_MEDIO}",
            "borderRadius": "16px",
            "boxSizing": "border-box",
        },
    )


# ============================================================
# SECCIÓN 1 — ATENUACIÓN
# ============================================================

def seccion_atenuacion():

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "01 · ATENUACIÓN",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "700",
                            "letterSpacing": "1.6px",
                            "color": BEIGE,
                            "marginBottom": "8px",
                        },
                    ),
                    html.H2(
                        "¿Qué ocurre cuando los Rayos X atraviesan el cuerpo?",
                        className="teoria-section-title",
                        style={"marginBottom": "10px"},
                    ),
                    html.P(
                        "Cuando el haz de Rayos X atraviesa al paciente, no todos "
                        "los fotones llegan al detector. Parte de la radiación es "
                        "absorbida o desviada por los tejidos. A esta disminución "
                        "de la intensidad del haz se le llama atenuación.",
                        className="teoria-intro",
                        style={"marginBottom": "0"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),

            _flujo(
                [
                    "TUBO DE RAYOS X",
                    "HAZ DE RAYOS X",
                    "PACIENTE",
                    "ATENUACIÓN",
                    "DETECTOR",
                    "IMAGEN",
                ]
            ),

            html.Div(
                [
                    _tarjeta(
                        "¿De qué depende?",
                        [
                            html.P(
                                "El espesor del material influye directamente: "
                                "cuanto mayor es el grosor atravesado, mayor es la "
                                "atenuación."
                            ),
                            html.P(
                                "También influyen la densidad, el número atómico "
                                "del material y la energía del haz."
                            ),
                        ],
                        "01",
                    ),
                    _tarjeta(
                        "¿Qué significa en la imagen?",
                        [
                            html.P(
                                "Los tejidos no atenúan los Rayos X de la misma forma. "
                                "Por eso diferentes cantidades de radiación llegan "
                                "a diferentes zonas del detector."
                            ),
                            html.P(
                                "Esas diferencias son fundamentales para formar "
                                "el contraste radiográfico."
                            ),
                        ],
                        "02",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                    "gap": "16px",
                    "marginBottom": "24px",
                },
            ),

            html.Div(
                [
                    _bloque_explicativo(
                        "APOYO VISUAL",
                        "Lee la imagen de izquierda a derecha",
                        "El haz sale del tubo, atraviesa diferentes tejidos y llega "
                        "al detector con una intensidad modificada. Esa información "
                        "será utilizada para construir la imagen radiográfica.",
                    ),
                    _imagen(
                        "atenuacion.png",
                        "Esquema de atenuación de los Rayos X",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "minmax(0, 0.42fr) minmax(0, 0.58fr)",
                    "gap": "16px",
                    "alignItems": "stretch",
                },
            ),
        ],
        className="teoria-section",
    )


# ============================================================
# SECCIÓN 2 — INTERACCIONES
# ============================================================

def seccion_interacciones():

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "02 · INTERACCIÓN RX–MATERIA",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "700",
                            "letterSpacing": "1.6px",
                            "color": BEIGE,
                            "marginBottom": "8px",
                        },
                    ),
                    html.H2(
                        "¿Cómo interactúan los Rayos X con la materia?",
                        className="teoria-section-title",
                        style={"marginBottom": "10px"},
                    ),
                    html.P(
                        "Durante el paso por el paciente pueden ocurrir diferentes "
                        "interacciones. Dos de las más importantes son el efecto "
                        "fotoeléctrico y el efecto Compton.",
                        className="teoria-intro",
                        style={"marginBottom": "0"},
                    ),
                ],
                style={"marginBottom": "22px"},
            ),

            html.Div(
                [
                    html.Div(
                        [
                            _tarjeta(
                                "Efecto fotoeléctrico",
                                [
                                    html.P(
                                        "El fotón de Rayos X es absorbido completamente "
                                        "por un átomo y expulsa un electrón de una "
                                        "capa interna."
                                    ),
                                    html.P(
                                        "El fotón desaparece y su energía se transfiere "
                                        "al material. Esta interacción contribuye "
                                        "fuertemente al contraste de la imagen."
                                    ),
                                ],
                                "01",
                            ),
                            html.Div(
                                style={"height": "12px"},
                            ),
                            _imagen(
                                "efecto_fotoelectrico.png",
                                "Efecto fotoeléctrico",
                                "280px",
                            ),
                        ],
                    ),

                    html.Div(
                        [
                            _tarjeta(
                                "Efecto Compton",
                                [
                                    html.P(
                                        "El fotón interactúa con un electrón y sale "
                                        "desviado en otra dirección con menor energía."
                                    ),
                                    html.P(
                                        "El fotón dispersado puede llegar al detector "
                                        "desde una dirección diferente y producir "
                                        "radiación dispersa."
                                    ),
                                ],
                                "02",
                            ),
                            html.Div(
                                style={"height": "12px"},
                            ),
                            _imagen(
                                "efecto_compton.png",
                                "Efecto Compton",
                                "280px",
                            ),
                        ],
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                    "gap": "18px",
                },
            ),

            html.Div(
                [
                    html.Span(
                        "IDEA CLAVE",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "800",
                            "letterSpacing": "1.3px",
                            "color": AZUL,
                            "backgroundColor": CREMA,
                            "padding": "6px 9px",
                            "borderRadius": "7px",
                        },
                    ),
                    html.Span(
                        " Fotoeléctrico → absorción completa   |   Compton → dispersión",
                        style={
                            "fontSize": "12px",
                            "fontWeight": "700",
                            "color": CREMA,
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "flexWrap": "wrap",
                    "gap": "8px",
                    "padding": "13px 15px",
                    "marginTop": "20px",
                    "backgroundColor": FONDO_CLARO,
                    "border": f"3px solid {AZUL_MEDIO}",
                    "borderRadius": "12px",
                },
            ),
        ],
        className="teoria-section",
    )


# ============================================================
# SECCIÓN 3 — RADIACIÓN DISPERSA
# ============================================================

def seccion_dispersion():

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "03 · RADIACIÓN DISPERSA",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "700",
                            "letterSpacing": "1.6px",
                            "color": BEIGE,
                            "marginBottom": "8px",
                        },
                    ),
                    html.H2(
                        "¿Qué es la radiación dispersa?",
                        className="teoria-section-title",
                        style={"marginBottom": "10px"},
                    ),
                    html.P(
                        "No toda la radiación que sale del paciente sigue el camino "
                        "original hacia el detector. Parte cambia de dirección por "
                        "interacciones como el efecto Compton.",
                        className="teoria-intro",
                        style={"marginBottom": "0"},
                    ),
                ],
                style={"marginBottom": "22px"},
            ),

            _flujo(
                [
                    "HAZ PRIMARIO",
                    "PACIENTE",
                    "INTERACCIÓN",
                    "RADIACIÓN DISPERSA",
                    "DETECTOR",
                    "IMAGEN",
                ]
            ),

            html.Div(
                [
                    _tarjeta(
                        "Radiación primaria",
                        [
                            html.P(
                                "Es la radiación que atraviesa el paciente sin "
                                "desviarse significativamente y continúa hacia "
                                "el detector."
                            ),
                            html.P(
                                "Es la principal responsable de transportar "
                                "información útil para formar la imagen."
                            ),
                        ],
                        "01",
                    ),
                    _tarjeta(
                        "Radiación dispersa",
                        [
                            html.P(
                                "Es la radiación que cambia de dirección después "
                                "de interactuar con la materia."
                            ),
                            html.P(
                                "Al llegar al detector desde direcciones no deseadas "
                                "puede reducir el contraste y añadir señal que "
                                "no representa correctamente la anatomía."
                            ),
                        ],
                        "02",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                    "gap": "16px",
                    "marginBottom": "22px",
                },
            ),

            html.Div(
                [
                    _imagen(
                        "radiacion_dispersa.png",
                        "Radiación primaria y radiación dispersa",
                        "360px",
                    ),
                    _bloque_explicativo(
                        "¿POR QUÉ IMPORTA?",
                        "La dispersión puede degradar la imagen",
                        "La radiación dispersa agrega señal no deseada al detector. "
                        "Esto puede disminuir el contraste radiográfico y dificultar "
                        "la diferenciación entre estructuras.",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "minmax(0, 0.62fr) minmax(0, 0.38fr)",
                    "gap": "16px",
                    "alignItems": "stretch",
                },
            ),
        ],
        className="teoria-section",
    )


# ============================================================
# SECCIÓN 4 — CONTRASTE
# ============================================================

def seccion_contraste():

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "04 · CONTRASTE RADIOGRÁFICO",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "700",
                            "letterSpacing": "1.6px",
                            "color": BEIGE,
                            "marginBottom": "8px",
                        },
                    ),
                    html.H2(
                        "¿Cómo se forma el contraste?",
                        className="teoria-section-title",
                        style={"marginBottom": "10px"},
                    ),
                    html.P(
                        "El contraste permite diferenciar unas estructuras de otras "
                        "en la radiografía. Se origina porque los distintos tejidos "
                        "atenúan el haz de Rayos X de manera diferente.",
                        className="teoria-intro",
                        style={"marginBottom": "0"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),

            _flujo(
                [
                    "TEJIDOS DIFERENTES",
                    "ATENUACIÓN DIFERENTE",
                    "RX TRANSMITIDOS DIFERENTES",
                    "SEÑAL DIFERENTE",
                    "VALORES DE PÍXEL",
                    "CONTRASTE",
                ]
            ),

            html.Div(
                [
                    _tarjeta(
                        "La idea física",
                        [
                            html.P(
                                "La densidad, el espesor y el número atómico de los "
                                "tejidos influyen en cuánto se atenúa el haz."
                            ),
                            html.P(
                                "Como resultado, no todas las zonas del detector "
                                "reciben la misma cantidad de radiación."
                            ),
                        ],
                        "01",
                    ),
                    _tarjeta(
                        "La idea en la imagen",
                        [
                            html.P(
                                "El detector convierte esas diferencias de radiación "
                                "en diferencias de señal."
                            ),
                            html.P(
                                "Después, esas diferencias se representan como "
                                "distintos valores de píxel y tonos de gris."
                            ),
                        ],
                        "02",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                    "gap": "16px",
                    "marginBottom": "22px",
                },
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "APOYO VISUAL",
                                style={
                                    "fontSize": "10px",
                                    "fontWeight": "700",
                                    "letterSpacing": "1.5px",
                                    "color": BEIGE,
                                    "marginBottom": "8px",
                                },
                            ),
                            html.H3(
                                "¿Qué estamos viendo en una radiografía?",
                                style={
                                    "margin": "0 0 14px 0",
                                    "fontSize": "22px",
                                    "lineHeight": "1.25",
                                    "color": CREMA,
                                },
                            ),
                            _imagen(
                                "contraste_radiografico.jpg",
                                "Radiografía de tórax para observar el contraste radiográfico",
                                "380px",
                            ),
                        ],
                        style={
                            "backgroundColor": FONDO_CLARO,
                            "border": f"3px solid {AZUL_MEDIO}",
                            "borderRadius": "16px",
                            "padding": "22px",
                            "boxSizing": "border-box",
                        },
                    ),

                    html.Div(
                        [
                            html.Div(
                                "LECTURA DE LA IMAGEN",
                                style={
                                    "fontSize": "10px",
                                    "fontWeight": "700",
                                    "letterSpacing": "1.5px",
                                    "color": BEIGE,
                                    "marginBottom": "8px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "01",
                                        style={
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "width": "42px",
                                            "height": "42px",
                                            "minWidth": "42px",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "10px",
                                            "fontWeight": "800",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.H4(
                                                "Hueso",
                                                style={
                                                    "margin": "0 0 4px 0",
                                                    "color": CREMA,
                                                    "fontSize": "17px",
                                                },
                                            ),
                                            html.P(
                                                "Atenúa una mayor cantidad de Rayos X y suele representarse más claro.",
                                                style={
                                                    "margin": "0",
                                                    "color": BEIGE,
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "gap": "12px",
                                    "alignItems": "flex-start",
                                    "padding": "15px",
                                    "backgroundColor": AZUL_OSCURO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "12px",
                                    "marginBottom": "12px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "02",
                                        style={
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "width": "42px",
                                            "height": "42px",
                                            "minWidth": "42px",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "10px",
                                            "fontWeight": "800",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.H4(
                                                "Aire",
                                                style={
                                                    "margin": "0 0 4px 0",
                                                    "color": CREMA,
                                                    "fontSize": "17px",
                                                },
                                            ),
                                            html.P(
                                                "Atenúa poco los Rayos X y suele representarse más oscuro.",
                                                style={
                                                    "margin": "0",
                                                    "color": BEIGE,
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "gap": "12px",
                                    "alignItems": "flex-start",
                                    "padding": "15px",
                                    "backgroundColor": AZUL_OSCURO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "12px",
                                    "marginBottom": "12px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "03",
                                        style={
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "width": "42px",
                                            "height": "42px",
                                            "minWidth": "42px",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "10px",
                                            "fontWeight": "800",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.H4(
                                                "Tejidos blandos",
                                                style={
                                                    "margin": "0 0 4px 0",
                                                    "color": CREMA,
                                                    "fontSize": "17px",
                                                },
                                            ),
                                            html.P(
                                                "Presentan una atenuación intermedia y aparecen en diferentes tonos de gris.",
                                                style={
                                                    "margin": "0",
                                                    "color": BEIGE,
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "gap": "12px",
                                    "alignItems": "flex-start",
                                    "padding": "15px",
                                    "backgroundColor": AZUL_OSCURO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "12px",
                                    "marginBottom": "18px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "IDEA CLAVE",
                                        style={
                                            "fontSize": "10px",
                                            "fontWeight": "800",
                                            "letterSpacing": "1.2px",
                                            "color": AZUL,
                                            "backgroundColor": CREMA,
                                            "padding": "7px 10px",
                                            "borderRadius": "8px",
                                            "whiteSpace": "nowrap",
                                        },
                                    ),
                                    html.P(
                                        "Mayor atenuación → menos radiación llega al detector → cambia el valor del píxel → aparece el contraste.",
                                        style={
                                            "margin": "0",
                                            "color": CREMA,
                                            "fontSize": "13px",
                                            "fontWeight": "700",
                                            "lineHeight": "1.5",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "flexWrap": "wrap",
                                    "padding": "14px",
                                    "backgroundColor": FONDO_CLARO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "12px",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": FONDO_CLARO,
                            "border": f"3px solid {AZUL_MEDIO}",
                            "borderRadius": "16px",
                            "padding": "22px",
                            "boxSizing": "border-box",
                        },
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "minmax(0, 1.15fr) minmax(0, 0.85fr)",
                    "gap": "18px",
                    "alignItems": "stretch",
                    "marginTop": "22px",
                },
            ),
        ],
        className="teoria-section",
    )


# ============================================================
# SECCIÓN 5 — DETECTORES
# ============================================================

def seccion_detectores():

    detectores = [
        (
            "01",
            "Película radiográfica",
            "ANALÓGICO",
            "Tecnología clásica que requiere revelado químico.",
        ),
        (
            "02",
            "CR / PSP",
            "SEMI-DIGITAL",
            "Placa de fósforo fotoestimulable que se escanea después de la exposición.",
        ),
        (
            "03",
            "CCD",
            "DIGITAL",
            "Sensor que convierte la luz en una señal eléctrica.",
        ),
        (
            "04",
            "TFT (Flat Panel)",
            "DIGITAL DIRECTO",
            "Panel plano de transistores utilizado en radiografía digital directa.",
        ),
        (
            "05",
            "CMOS",
            "DIGITAL",
            "Sensor semiconductor utilizado para convertir la información en señal.",
        ),
    ]

    tarjetas_detectores = []

    for numero, nombre, tipo, descripcion in detectores:

        tarjetas_detectores.append(
            html.Div(
                [
                    html.Div(
                        numero,
                        style={
                            "width": "42px",
                            "height": "42px",
                            "minWidth": "42px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "backgroundColor": CREMA,
                            "color": AZUL,
                            "borderRadius": "10px",
                            "fontSize": "13px",
                            "fontWeight": "800",
                            "boxSizing": "border-box",
                        },
                    ),

                    html.Div(
                        [
                            html.Div(
                                nombre,
                                style={
                                    "fontSize": "15px",
                                    "fontWeight": "700",
                                    "lineHeight": "1.25",
                                    "color": CREMA,
                                    "marginBottom": "4px",
                                },
                            ),

                            html.Div(
                                tipo,
                                style={
                                    "display": "inline-block",
                                    "padding": "4px 8px",
                                    "backgroundColor": CREMA,
                                    "color": AZUL,
                                    "borderRadius": "7px",
                                    "fontSize": "9px",
                                    "fontWeight": "800",
                                    "letterSpacing": "0.5px",
                                    "marginBottom": "5px",
                                },
                            ),

                            html.Div(
                                descripcion,
                                style={
                                    "fontSize": "11px",
                                    "lineHeight": "1.45",
                                    "color": BEIGE,
                                },
                            ),
                        ],
                        style={
                            "flex": "1",
                            "minWidth": "0",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "flex-start",
                    "gap": "12px",
                    "padding": "13px 14px",
                    "backgroundColor": AZUL_OSCURO,
                    "border": f"3px solid {AZUL_MEDIO}",
                    "borderRadius": "12px",
                    "boxSizing": "border-box",
                    "marginBottom": "9px",
                },
            )
        )

    return html.Div(
        [
            # ========================================================
            # ENCABEZADO
            # ========================================================

            html.Div(
                [
                    html.Div(
                        "05 · DETECTORES",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "700",
                            "letterSpacing": "1.6px",
                            "color": BEIGE,
                            "marginBottom": "8px",
                        },
                    ),

                    html.H2(
                        "¿Cómo se convierte la radiación en una señal?",
                        className="teoria-section-title",
                        style={
                            "marginBottom": "10px",
                        },
                    ),

                    html.P(
                        "El detector recibe los Rayos X que atravesaron al paciente "
                        "y los transforma en una señal que posteriormente puede "
                        "convertirse en una imagen.",
                        className="teoria-intro",
                        style={
                            "marginBottom": "24px",
                        },
                    ),
                ],
            ),

            # ========================================================
            # BLOQUE PRINCIPAL
            # ========================================================

            html.Div(
                [

                    # ------------------------------------------------
                    # COLUMNA IZQUIERDA
                    # ------------------------------------------------

                    html.Div(
                        [
                            html.Div(
                                "TECNOLOGÍAS DE DETECCIÓN",
                                style={
                                    "fontSize": "10px",
                                    "fontWeight": "700",
                                    "letterSpacing": "1.4px",
                                    "color": BEIGE,
                                    "marginBottom": "6px",
                                },
                            ),

                            html.H3(
                                "Tipos de detectores",
                                style={
                                    "margin": "0 0 8px 0",
                                    "fontSize": "24px",
                                    "lineHeight": "1.2",
                                    "color": CREMA,
                                },
                            ),

                            html.P(
                                "Existen diferentes tecnologías para transformar "
                                "la radiación recibida en una señal útil para "
                                "formar la imagen.",
                                style={
                                    "margin": "0 0 18px 0",
                                    "fontSize": "12px",
                                    "lineHeight": "1.55",
                                    "color": BEIGE,
                                },
                            ),

                            html.Div(
                                tarjetas_detectores,
                            ),
                        ],
                        style={
                            "backgroundColor": FONDO_CLARO,
                            "border": f"3px solid {AZUL_MEDIO}",
                            "borderRadius": "16px",
                            "padding": "22px",
                            "boxSizing": "border-box",
                        },
                    ),

                    # ------------------------------------------------
                    # COLUMNA DERECHA
                    # ------------------------------------------------

                    html.Div(
                        [
                            html.Div(
                                "DEL HAZ A LA IMAGEN",
                                style={
                                    "fontSize": "10px",
                                    "fontWeight": "700",
                                    "letterSpacing": "1.4px",
                                    "color": BEIGE,
                                    "marginBottom": "6px",
                                },
                            ),

                            html.H3(
                                "¿Qué hace el detector?",
                                style={
                                    "margin": "0 0 8px 0",
                                    "fontSize": "24px",
                                    "lineHeight": "1.2",
                                    "color": CREMA,
                                },
                            ),

                            html.P(
                                "El detector recibe los fotones de Rayos X y los "
                                "convierte en una señal eléctrica o digital que "
                                "puede ser procesada para formar la imagen.",
                                style={
                                    "margin": "0 0 16px 0",
                                    "fontSize": "12px",
                                    "lineHeight": "1.55",
                                    "color": BEIGE,
                                },
                            ),

                            _imagen(
                                "detectores.png",
                                "Tipos de detectores de Rayos X",
                                "300px",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "01",
                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "minWidth": "34px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.P(
                                        "La tecnología del detector determina cómo "
                                        "se transforma la radiación recibida y cómo "
                                        "se obtiene la información de la imagen.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.5",
                                            "color": BEIGE,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "padding": "12px",
                                    "marginTop": "12px",
                                    "backgroundColor": AZUL_OSCURO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "11px",
                                    "boxSizing": "border-box",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": FONDO_CLARO,
                            "border": f"3px solid {AZUL_MEDIO}",
                            "borderRadius": "16px",
                            "padding": "22px",
                            "boxSizing": "border-box",
                        },
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "minmax(0, 1fr) minmax(0, 1fr)",
                    "gap": "18px",
                    "alignItems": "stretch",
                    "marginBottom": "18px",
                },
            ),

            # ========================================================
            # PUNTOS CLAVE
            # ========================================================

            html.Div(
                [
                    html.Div(
                        "PUNTOS CLAVE",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "800",
                            "letterSpacing": "1.4px",
                            "color": BEIGE,
                            "marginBottom": "12px",
                        },
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "01",
                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "minWidth": "34px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.P(
                                        "El detector transforma la radiación recibida "
                                        "en una señal.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.5",
                                            "color": CREMA,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "flex": "1",
                                    "minWidth": "0",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "02",
                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "minWidth": "34px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.P(
                                        "La señal puede ser analógica o digital "
                                        "según la tecnología utilizada.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.5",
                                            "color": CREMA,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "flex": "1",
                                    "minWidth": "0",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "03",
                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "minWidth": "34px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.P(
                                        "La señal obtenida se procesa para generar "
                                        "la imagen radiográfica.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.5",
                                            "color": CREMA,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "flex": "1",
                                    "minWidth": "0",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "gap": "14px",
                            "width": "100%",
                        },
                    ),
                ],
                style={
                    "backgroundColor": FONDO_CLARO,
                    "border": f"3px solid {AZUL_MEDIO}",
                    "borderRadius": "16px",
                    "padding": "18px 20px",
                    "boxSizing": "border-box",
                    "marginBottom": "18px",
                },
            ),

            # ========================================================
            # IDEA CLAVE
            # ========================================================

            html.Div(
                [
                    html.Span(
                        "IDEA CLAVE",
                        style={
                            "display": "inline-flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "padding": "9px 13px",
                            "backgroundColor": CREMA,
                            "color": AZUL,
                            "borderRadius": "9px",
                            "fontSize": "10px",
                            "fontWeight": "800",
                            "letterSpacing": "1px",
                            "whiteSpace": "nowrap",
                        },
                    ),

                    html.P(
                        "El detector es el puente entre la radiación que sale del "
                        "paciente y la señal que finalmente permite construir la imagen.",
                        style={
                            "margin": "0",
                            "fontSize": "13px",
                            "fontWeight": "700",
                            "lineHeight": "1.5",
                            "color": CREMA,
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "14px",
                    "flexWrap": "wrap",
                    "padding": "15px 18px",
                    "backgroundColor": FONDO_CLARO,
                    "border": f"3px solid {AZUL_MEDIO}",
                    "borderRadius": "14px",
                    "boxSizing": "border-box",
                },
            ),
        ],
        className="teoria-section",
    )

# ============================================================
# SECCIÓN 6 — RADIOGRAFÍA DIGITAL
# ============================================================

def seccion_radiografia_digital():

    return html.Div(
        [
            # ========================================================
            # ENCABEZADO
            # ========================================================

            html.Div(
                [
                    html.Div(
                        "06 · RADIOGRAFÍA DIGITAL",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "700",
                            "letterSpacing": "1.6px",
                            "color": BEIGE,
                            "marginBottom": "8px",
                        },
                    ),

                    html.H2(
                        "¿Cómo se transforma la señal en una imagen digital?",
                        className="teoria-section-title",
                        style={
                            "marginBottom": "10px",
                        },
                    ),

                    html.P(
                        "Después de recibir los Rayos X, el detector genera una señal "
                        "que es procesada y convertida en datos digitales. Estos datos "
                        "se organizan para construir la imagen radiográfica.",
                        className="teoria-intro",
                        style={
                            "marginBottom": "24px",
                        },
                    ),
                ],
            ),

            # ========================================================
            # SECUENCIA PRINCIPAL
            # ========================================================

            _flujo(
                [
                    "RAYOS X",
                    "DETECTOR",
                    "SEÑAL",
                    "CONVERSIÓN A/D",
                    "DATOS DIGITALES",
                    "MATRIZ DE PÍXELES",
                    "IMAGEN",
                ],
                altura="72px",
            ),

            # ========================================================
            # DOS CONCEPTOS CLAVE
            # ========================================================

            html.Div(
                [
                    _tarjeta(
                        "Matriz de píxeles",
                        [
                            html.P(
                                "Una imagen digital está formada por una matriz "
                                "de pequeños elementos llamados píxeles."
                            ),

                            html.P(
                                "Cada píxel contiene un valor numérico que representa "
                                "la señal registrada en una determinada posición."
                            ),
                        ],
                        "01",
                    ),

                    _tarjeta(
                        "Niveles de gris",
                        [
                            html.P(
                                "Los valores almacenados en los píxeles se representan "
                                "visualmente mediante diferentes niveles de gris."
                            ),

                            html.P(
                                "Las diferencias entre estos valores permiten distinguir "
                                "estructuras con diferente atenuación."
                            ),
                        ],
                        "02",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                    "gap": "16px",
                    "marginBottom": "22px",
                },
            ),

            # ========================================================
            # IMAGEN + EXPLICACIÓN
            # ========================================================

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "DEL DETECTOR A LA IMAGEN",
                                style={
                                    "fontSize": "10px",
                                    "fontWeight": "700",
                                    "letterSpacing": "1.4px",
                                    "color": BEIGE,
                                    "marginBottom": "8px",
                                },
                            ),

                            html.H3(
                                "El proceso de digitalización",
                                style={
                                    "margin": "0 0 14px 0",
                                    "fontSize": "22px",
                                    "lineHeight": "1.25",
                                    "color": CREMA,
                                },
                            ),

                            _imagen(
                                "formacion_imagen.png",
                                "Proceso de formación de la imagen radiográfica",
                                "360px",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "DE LA SEÑAL A LA IMAGEN",
                                        style={
                                            "display": "inline-block",
                                            "padding": "7px 10px",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "8px",
                                            "fontSize": "9px",
                                            "fontWeight": "800",
                                            "letterSpacing": "1px",
                                            "marginTop": "14px",
                                            "marginBottom": "8px",
                                        },
                                    ),

                                    html.P(
                                        "El detector transforma la radiación recibida en información "
                                        "digital. Estos datos se organizan como píxeles y permiten "
                                        "construir la imagen radiográfica.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "13px",
                                            "lineHeight": "1.55",
                                            "color": BEIGE,
                                        },
                                    ),
                                ],
                                style={
                                    "padding": "14px 4px 2px 4px",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": FONDO_CLARO,
                            "border": f"3px solid {AZUL_MEDIO}",
                            "borderRadius": "16px",
                            "padding": "22px",
                            "boxSizing": "border-box",
                        },
                    ),

                    html.Div(
                        [
                            html.Div(
                                "¿QUÉ SUCEDE EN CADA PASO?",
                                style={
                                    "fontSize": "10px",
                                    "fontWeight": "700",
                                    "letterSpacing": "1.4px",
                                    "color": BEIGE,
                                    "marginBottom": "12px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "01",
                                        style={
                                            "width": "38px",
                                            "height": "38px",
                                            "minWidth": "38px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.Div(
                                        [
                                            html.H4(
                                                "Captura",
                                                style={
                                                    "margin": "0 0 4px 0",
                                                    "fontSize": "17px",
                                                    "color": CREMA,
                                                },
                                            ),

                                            html.P(
                                                "El detector recibe la radiación que "
                                                "atravesó al paciente.",
                                                style={
                                                    "margin": "0",
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                    "color": BEIGE,
                                                },
                                            ),
                                        ]
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "flex-start",
                                    "gap": "11px",
                                    "padding": "14px",
                                    "backgroundColor": AZUL_OSCURO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "11px",
                                    "marginBottom": "10px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "02",
                                        style={
                                            "width": "38px",
                                            "height": "38px",
                                            "minWidth": "38px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.Div(
                                        [
                                            html.H4(
                                                "Digitalización",
                                                style={
                                                    "margin": "0 0 4px 0",
                                                    "fontSize": "17px",
                                                    "color": CREMA,
                                                },
                                            ),

                                            html.P(
                                                "La señal se convierte en datos digitales "
                                                "que puede procesar el sistema.",
                                                style={
                                                    "margin": "0",
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                    "color": BEIGE,
                                                },
                                            ),
                                        ]
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "flex-start",
                                    "gap": "11px",
                                    "padding": "14px",
                                    "backgroundColor": AZUL_OSCURO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "11px",
                                    "marginBottom": "10px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "03",
                                        style={
                                            "width": "38px",
                                            "height": "38px",
                                            "minWidth": "38px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.Div(
                                        [
                                            html.H4(
                                                "Representación",
                                                style={
                                                    "margin": "0 0 4px 0",
                                                    "fontSize": "17px",
                                                    "color": CREMA,
                                                },
                                            ),

                                            html.P(
                                                "Los datos se organizan como una matriz "
                                                "de píxeles y se muestran como una imagen.",
                                                style={
                                                    "margin": "0",
                                                    "fontSize": "12px",
                                                    "lineHeight": "1.5",
                                                    "color": BEIGE,
                                                },
                                            ),
                                        ]
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "flex-start",
                                    "gap": "11px",
                                    "padding": "14px",
                                    "backgroundColor": AZUL_OSCURO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "11px",
                                    "marginBottom": "16px",
                                },
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "RESULTADO",
                                        style={
                                            "display": "inline-block",
                                            "padding": "7px 9px",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "8px",
                                            "fontSize": "9px",
                                            "fontWeight": "800",
                                            "letterSpacing": "1px",
                                            "marginBottom": "8px",
                                        },
                                    ),

                                    html.P(
                                        "El resultado final es una imagen digital "
                                        "formada por valores de píxel que pueden "
                                        "ser visualizados y procesados.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.55",
                                            "color": BEIGE,
                                        },
                                    ),
                                ],
                                style={
                                    "padding": "14px",
                                    "backgroundColor": FONDO_CLARO,
                                    "border": f"3px solid {AZUL_MEDIO}",
                                    "borderRadius": "11px",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": FONDO_CLARO,
                            "border": f"3px solid {AZUL_MEDIO}",
                            "borderRadius": "16px",
                            "padding": "22px",
                            "boxSizing": "border-box",
                        },
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "minmax(0, 1.15fr) minmax(0, 0.85fr)",
                    "gap": "18px",
                    "alignItems": "stretch",
                    "marginBottom": "18px",
                },
            ),

            # ========================================================
            # PUNTOS CLAVE
            # ========================================================

            html.Div(
                [
                    html.Div(
                        "PUNTOS CLAVE",
                        style={
                            "fontSize": "10px",
                            "fontWeight": "800",
                            "letterSpacing": "1.4px",
                            "color": BEIGE,
                            "marginBottom": "12px",
                        },
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "01",
                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "minWidth": "34px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.P(
                                        "La imagen digital está formada por una matriz de píxeles.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.5",
                                            "color": CREMA,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "flex": "1",
                                    "minWidth": "0",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "02",
                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "minWidth": "34px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.P(
                                        "Cada píxel contiene información numérica de la señal.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.5",
                                            "color": CREMA,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "flex": "1",
                                    "minWidth": "0",
                                },
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "03",
                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "minWidth": "34px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": CREMA,
                                            "color": AZUL,
                                            "borderRadius": "9px",
                                            "fontSize": "11px",
                                            "fontWeight": "800",
                                        },
                                    ),

                                    html.P(
                                        "Los diferentes valores de píxel permiten representar los tonos de gris.",
                                        style={
                                            "margin": "0",
                                            "fontSize": "12px",
                                            "lineHeight": "1.5",
                                            "color": CREMA,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "10px",
                                    "flex": "1",
                                    "minWidth": "0",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "gap": "14px",
                            "width": "100%",
                        },
                    ),
                ],
                style={
                    "backgroundColor": FONDO_CLARO,
                    "border": f"3px solid {AZUL_MEDIO}",
                    "borderRadius": "16px",
                    "padding": "18px 20px",
                    "boxSizing": "border-box",
                    "marginBottom": "18px",
                },
            ),

            # ========================================================
            # IDEA CLAVE
            # ========================================================

            html.Div(
                [
                    html.Span(
                        "IDEA CLAVE",
                        style={
                            "display": "inline-flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "padding": "9px 13px",
                            "backgroundColor": CREMA,
                            "color": AZUL,
                            "borderRadius": "9px",
                            "fontSize": "10px",
                            "fontWeight": "800",
                            "letterSpacing": "1px",
                            "whiteSpace": "nowrap",
                        },
                    ),

                    html.P(
                        "Detector → señal → digitalización → matriz de píxeles → imagen.",
                        style={
                            "margin": "0",
                            "fontSize": "13px",
                            "fontWeight": "700",
                            "lineHeight": "1.5",
                            "color": CREMA,
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "14px",
                    "flexWrap": "wrap",
                    "padding": "15px 18px",
                    "backgroundColor": FONDO_CLARO,
                    "border": f"3px solid {AZUL_MEDIO}",
                    "borderRadius": "14px",
                    "boxSizing": "border-box",
                },
            ),
        ],
        className="teoria-section",
    )

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def mostrar_formacion():

    return html.Div(
        [
            # --------------------------------------------------------
            # HERO — MISMO FORMATO QUE TEORÍA
            # --------------------------------------------------------

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "FORMACIÓN · RADIOLOGÍA",
                                style={
                                    "fontSize": "11px",
                                    "fontWeight": "700",
                                    "letterSpacing": "2px",
                                    "color": BEIGE,
                                    "marginBottom": "14px",
                                },
                            ),

                            html.H1(
                                "Formación de la Imagen Radiográfica",
                                className="teoria-hero-title",
                                style={
                                    "margin": "0",
                                    "fontSize": "42px",
                                    "lineHeight": "1.1",
                                    "fontWeight": "700",
                                    "color": CREMA,
                                },
                            ),

                            html.P(
                                "Comprende cómo los Rayos X atraviesan el cuerpo, "
                                "interactúan con los tejidos y se convierten en una "
                                "imagen médica.",
                                className="teoria-hero-subtitle",
                                style={
                                    "margin": "16px 0 0 0",
                                    "maxWidth": "760px",
                                    "fontSize": "15px",
                                    "lineHeight": "1.7",
                                    "color": BEIGE,
                                },
                            ),

                            html.Div(
                                style={
                                    "width": "70px",
                                    "height": "3px",
                                    "backgroundColor": BEIGE,
                                    "borderRadius": "3px",
                                    "marginTop": "24px",
                                }
                            ),
                        ],
                        style={
                            "position": "relative",
                            "zIndex": "2",
                        },
                    ),

                    html.Img(
                        src="/assets/formacion/manitos1.svg", # <-- Tu imagen SVG
                        alt="Icono de fondo Formación",
                        style={
                            "position": "absolute",
                            "right": "55px",
                            "top": "50%",
                            "transform": "translateY(-50%)",
                            "width": "180px",
                            "height": "auto",
                            #"opacity": "0.13",
                            #"filter": "grayscale(1)",
                            "pointerEvents": "none",
                        },
                    ),
                ],
                className="teoria-hero",
                style={
                    "position": "relative",
                    "overflow": "hidden",
                    "background": (
                        "linear-gradient("
                        "0deg, "
                        "rgb(255, 251, 247) 40%, "
                        "rgb(169, 212, 192) 100%"
                        ")"
                    ),
                    "border": "3px solid #A9D4C0",
                    "borderRadius": "18px",
                    "padding": "42px 46px",
                    "marginBottom": "28px",
                    "minHeight": "220px",
                    "boxSizing": "border-box",
                    "display": "flex",
                    "alignItems": "center",
                    "boxShadow": "0 12px 30px rgba(0, 0, 0, 0.18)",
                },
            ),

            # --------------------------------------------------------
            # PESTAÑAS — MISMO FORMATO QUE TEORÍA
            # --------------------------------------------------------

                        dcc.Tabs(
                id="formacion-tabs",
                value="atenuacion",
                className="teoria-tabs",
                children=[
                    dcc.Tab(
                        label=html.Span([
                            html.I(className="fa-solid fa-wave-square", style={"marginRight": "8px"}),
                            "Atenuación"
                        ]),
                        value="atenuacion",
                        className="teoria-tab",
                        selected_className="teoria-tab-selected",
                        children=seccion_atenuacion(),
                    ),
                    dcc.Tab(
                        label=html.Span([
                            html.I(className="fa-solid fa-atom", style={"marginRight": "8px"}),
                            "Interacciones"
                        ]),
                        value="interacciones",
                        className="teoria-tab",
                        selected_className="teoria-tab-selected",
                        children=seccion_interacciones(),
                    ),
                    dcc.Tab(
                        label=html.Span([
                            html.I(className="fa-solid fa-shuffle", style={"marginRight": "8px"}),
                            "Dispersión"
                        ]),
                        value="dispersion",
                        className="teoria-tab",
                        selected_className="teoria-tab-selected",
                        children=seccion_dispersion(),
                    ),
                    dcc.Tab(
                        label=html.Span([
                            html.I(className="fa-solid fa-circle-half-stroke", style={"marginRight": "8px"}),
                            "Contraste"
                        ]),
                        value="contraste",
                        className="teoria-tab",
                        selected_className="teoria-tab-selected",
                        children=seccion_contraste(),
                    ),
                    dcc.Tab(
                        label=html.Span([
                            html.I(className="fa-solid fa-microchip", style={"marginRight": "8px"}),
                            "Detectores"
                        ]),
                        value="detectores",
                        className="teoria-tab",
                        selected_className="teoria-tab-selected",
                        children=seccion_detectores(),
                    ),
                    dcc.Tab(
                        label=html.Span([
                            html.I(className="fa-solid fa-laptop-medical", style={"marginRight": "8px"}),
                            "Radiografía digital"
                        ]),
                        value="digital",
                        className="teoria-tab",
                        selected_className="teoria-tab-selected",
                        children=seccion_radiografia_digital(),
                    ),
                ],
            ),
        ],
        id="seccion-formacion-imagen",
    )

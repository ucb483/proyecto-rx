# ============================================================
# PLATAFORMA EDUCATIVA DE RAYOS X
# Módulo: Actividades
# ============================================================

import os
import csv
import random
from datetime import datetime

from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    ALL,
    no_update,
)


# ============================================================
# PALETA DEL PROYECTO
# ============================================================

THEME = {
    "bg": "#F1F7F3",
    "bg_secondary": "rgb(252, 244, 235)",
    "card": "rgb(255, 251, 247)",
    "blue": "#A9D4C0",
    "cream": "#2B3A35",
    "beige": "#5E8776",
    "text": "#2B3A35",
    "text_secondary": "#5E8776",
    "border": "#5E8776",
    "success": "#74B899",
    "error": "#D9A0A0",
}


# ============================================================
# BANCO DE PREGUNTAS
# ============================================================

BANCO_PREGUNTAS = [

    # ========================================================
    # FUNDAMENTOS
    # ========================================================

    {
        "tema": "Fundamentos",
        "pregunta": "¿Qué son los Rayos X?",
        "opciones": [
            "Radiación electromagnética ionizante",
            "Ondas mecánicas",
            "Partículas exclusivamente materiales",
            "Radiación sonora",
        ],
        "respuesta": "Radiación electromagnética ionizante",
        "explicacion": (
            "Los Rayos X son una forma de radiación electromagnética "
            "con suficiente energía para producir ionización."
        ),
    },

    {
        "tema": "Fundamentos",
        "pregunta": "¿Cuál de las siguientes características corresponde a los Rayos X?",
        "opciones": [
            "No tienen carga eléctrica",
            "Tienen carga positiva",
            "Tienen carga negativa",
            "Son ondas sonoras",
        ],
        "respuesta": "No tienen carga eléctrica",
        "explicacion": (
            "Los Rayos X son radiación electromagnética y, por lo tanto, "
            "no poseen carga eléctrica."
        ),
    },

    {
        "tema": "Fundamentos",
        "pregunta": "¿Cuál es una aplicación médica importante de los Rayos X?",
        "opciones": [
            "Obtención de imágenes internas del cuerpo",
            "Medición directa de la temperatura",
            "Producción de sonido",
            "Medición de la presión atmosférica",
        ],
        "respuesta": "Obtención de imágenes internas del cuerpo",
        "explicacion": (
            "La radiografía utiliza Rayos X para obtener información "
            "sobre las estructuras internas del organismo."
        ),
    },

    {
        "tema": "Fundamentos",
        "pregunta": "¿Por qué los Rayos X se consideran radiación ionizante?",
        "opciones": [
            "Porque pueden transferir suficiente energía para ionizar átomos",
            "Porque producen únicamente calor",
            "Porque tienen una frecuencia igual a la del sonido",
            "Porque siempre atraviesan completamente la materia",
        ],
        "respuesta": "Porque pueden transferir suficiente energía para ionizar átomos",
        "explicacion": (
            "La energía de los fotones de Rayos X puede ser suficiente "
            "para remover electrones de los átomos."
        ),
    },

    {
        "tema": "Fundamentos",
        "pregunta": "¿Quién descubrió los Rayos X en 1895?",
        "opciones": [
            "Wilhelm Conrad Röntgen",
            "Albert Einstein",
            "Isaac Newton",
            "Michael Faraday",
        ],
        "respuesta": "Wilhelm Conrad Röntgen",
        "explicacion": (
            "Wilhelm Conrad Röntgen descubrió los Rayos X en 1895."
        ),
    },

    {
        "tema": "Fundamentos",
        "pregunta": "¿Qué propiedad permite que los Rayos X sean utilizados para visualizar estructuras internas?",
        "opciones": [
            "Su capacidad de atravesar la materia con diferentes grados de atenuación",
            "Su capacidad de producir únicamente sonido",
            "Su capacidad de detenerse siempre en la superficie",
            "Su ausencia total de interacción con la materia",
        ],
        "respuesta": "Su capacidad de atravesar la materia con diferentes grados de atenuación",
        "explicacion": (
            "Los distintos tejidos atenúan los Rayos X de manera diferente, "
            "lo que permite generar contraste en la imagen."
        ),
    },


    # ========================================================
    # PRODUCCIÓN
    # ========================================================

    {
        "tema": "Producción",
        "pregunta": "¿Qué componente del tubo de Rayos X emite electrones?",
        "opciones": [
            "Cátodo",
            "Ánodo",
            "Colimador",
            "Detector",
        ],
        "respuesta": "Cátodo",
        "explicacion": (
            "El cátodo contiene el filamento que, al calentarse, "
            "favorece la emisión de electrones."
        ),
    },

    {
        "tema": "Producción",
        "pregunta": "¿Cuál es la función principal del ánodo?",
        "opciones": [
            "Recibir los electrones y actuar como blanco",
            "Emitir electrones desde el filamento",
            "Almacenar la imagen digital",
            "Reducir el tamaño del paciente",
        ],
        "respuesta": "Recibir los electrones y actuar como blanco",
        "explicacion": (
            "Los electrones acelerados desde el cátodo impactan contra "
            "el blanco del ánodo y allí se producen los Rayos X."
        ),
    },

    {
        "tema": "Producción",
        "pregunta": "¿Qué ocurre cuando los electrones emitidos por el cátodo son acelerados hacia el ánodo?",
        "opciones": [
            "Adquieren energía cinética",
            "Pierden toda su energía inmediatamente",
            "Se convierten en sonido",
            "Desaparecen antes de llegar al ánodo",
        ],
        "respuesta": "Adquieren energía cinética",
        "explicacion": (
            "La diferencia de potencial entre cátodo y ánodo acelera "
            "los electrones y aumenta su energía cinética."
        ),
    },

    {
        "tema": "Producción",
        "pregunta": "¿Qué fenómeno produce radiación de frenado o Bremsstrahlung?",
        "opciones": [
            "La desaceleración de electrones cerca del núcleo del blanco",
            "La emisión de luz visible por el paciente",
            "La vibración mecánica del detector",
            "La reflexión de ondas de sonido",
        ],
        "respuesta": "La desaceleración de electrones cerca del núcleo del blanco",
        "explicacion": (
            "Bremsstrahlung se produce cuando los electrones son "
            "desacelerados o desviados por el campo eléctrico del núcleo."
        ),
    },

    {
        "tema": "Producción",
        "pregunta": "¿Qué caracteriza a la radiación característica?",
        "opciones": [
            "Se produce por transiciones electrónicas entre niveles de energía del átomo",
            "Se produce exclusivamente por calor",
            "Se genera en el detector",
            "Es producida por ondas mecánicas",
        ],
        "respuesta": "Se produce por transiciones electrónicas entre niveles de energía del átomo",
        "explicacion": (
            "La radiación característica aparece cuando electrones de niveles "
            "superiores ocupan vacantes en niveles internos del átomo."
        ),
    },

    {
        "tema": "Producción",
        "pregunta": "¿Aproximadamente qué porcentaje de la energía de los electrones se transforma en Rayos X en un tubo convencional?",
        "opciones": [
            "Aproximadamente 1 %",
            "Aproximadamente 25 %",
            "Aproximadamente 50 %",
            "Aproximadamente 99 %",
        ],
        "respuesta": "Aproximadamente 1 %",
        "explicacion": (
            "En un tubo convencional, solo una pequeña fracción de la energía "
            "se convierte en Rayos X y la mayor parte se transforma en calor."
        ),
    },


    # ========================================================
    # FORMACIÓN DE IMAGEN
    # ========================================================

    {
        "tema": "Formación",
        "pregunta": "¿Qué significa atenuación de los Rayos X?",
        "opciones": [
            "Reducción de la intensidad del haz al atravesar la materia",
            "Aumento de la intensidad al atravesar el cuerpo",
            "Conversión de Rayos X en sonido",
            "Eliminación completa del detector",
        ],
        "respuesta": "Reducción de la intensidad del haz al atravesar la materia",
        "explicacion": (
            "La atenuación representa la disminución de la intensidad "
            "del haz debido a la absorción y dispersión."
        ),
    },

    {
        "tema": "Formación",
        "pregunta": "¿Qué interacción está relacionada con la absorción completa de un fotón de Rayos X?",
        "opciones": [
            "Efecto fotoeléctrico",
            "Efecto Compton",
            "Reflexión",
            "Interferencia acústica",
        ],
        "respuesta": "Efecto fotoeléctrico",
        "explicacion": (
            "En el efecto fotoeléctrico el fotón transfiere su energía "
            "a un electrón y desaparece."
        ),
    },

    {
        "tema": "Formación",
        "pregunta": "¿Qué ocurre en el efecto Compton?",
        "opciones": [
            "El fotón interactúa con un electrón y se dispersa con menor energía",
            "El fotón desaparece sin interacción",
            "El fotón se convierte en sonido",
            "El electrón se convierte en un protón",
        ],
        "respuesta": "El fotón interactúa con un electrón y se dispersa con menor energía",
        "explicacion": (
            "En la dispersión Compton, el fotón transfiere parte de su energía "
            "a un electrón y cambia de dirección."
        ),
    },

    {
        "tema": "Formación",
        "pregunta": "¿Qué tejido suele presentar mayor atenuación de Rayos X?",
        "opciones": [
            "Hueso",
            "Aire",
            "Pulmón",
            "Tejido blando",
        ],
        "respuesta": "Hueso",
        "explicacion": (
            "El hueso presenta mayor atenuación debido a su composición "
            "y densidad, por lo que suele aparecer más radiopaco."
        ),
    },

    {
        "tema": "Formación",
        "pregunta": "¿Qué efecto contribuye significativamente a la radiación dispersa?",
        "opciones": [
            "Efecto Compton",
            "Efecto fotoeléctrico exclusivamente",
            "Emisión termoiónica",
            "Bremsstrahlung dentro del detector",
        ],
        "respuesta": "Efecto Compton",
        "explicacion": (
            "El efecto Compton cambia la dirección del fotón y contribuye "
            "a la radiación dispersa."
        ),
    },

    {
        "tema": "Formación",
        "pregunta": "¿Qué sucede con la intensidad del haz cuando aumenta la atenuación?",
        "opciones": [
            "Disminuye",
            "Aumenta siempre",
            "Permanece exactamente igual",
            "Se convierte completamente en luz visible",
        ],
        "respuesta": "Disminuye",
        "explicacion": (
            "Una mayor atenuación significa que una menor cantidad de "
            "fotones logra atravesar el material."
        ),
    },


    # ========================================================
    # DETECTORES
    # ========================================================

    {
        "tema": "Detectores",
        "pregunta": "¿Cuál es la función principal de un detector digital?",
        "opciones": [
            "Convertir la radiación recibida en una señal que permita formar una imagen",
            "Generar los electrones del tubo",
            "Aumentar el voltaje del paciente",
            "Eliminar completamente los Rayos X",
        ],
        "respuesta": "Convertir la radiación recibida en una señal que permita formar una imagen",
        "explicacion": (
            "El detector recibe la radiación remanente y la transforma "
            "en una señal utilizada para construir la imagen digital."
        ),
    },

    {
        "tema": "Detectores",
        "pregunta": "¿Qué caracteriza a un detector indirecto?",
        "opciones": [
            "Convierte primero los Rayos X en luz y luego en señal eléctrica",
            "Convierte directamente Rayos X en señal eléctrica",
            "No utiliza ningún material detector",
            "Convierte Rayos X en sonido",
        ],
        "respuesta": "Convierte primero los Rayos X en luz y luego en señal eléctrica",
        "explicacion": (
            "En los detectores indirectos existe una etapa de conversión "
            "de Rayos X a luz antes de generar la señal eléctrica."
        ),
    },

    {
        "tema": "Detectores",
        "pregunta": "¿Qué caracteriza a un detector directo?",
        "opciones": [
            "Convierte los Rayos X directamente en carga eléctrica",
            "Convierte primero los Rayos X en sonido",
            "Solo produce imágenes analógicas",
            "No necesita material semiconductor",
        ],
        "respuesta": "Convierte los Rayos X directamente en carga eléctrica",
        "explicacion": (
            "En la conversión directa, el material fotoconductor genera "
            "carga eléctrica a partir de la radiación X."
        ),
    },

    {
        "tema": "Detectores",
        "pregunta": "¿Qué significa que un detector tenga buena resolución espacial?",
        "opciones": [
            "Puede distinguir detalles pequeños y cercanos entre sí",
            "Tiene mayor temperatura",
            "Produce más radiación dispersa",
            "Utiliza más corriente del tubo",
        ],
        "respuesta": "Puede distinguir detalles pequeños y cercanos entre sí",
        "explicacion": (
            "La resolución espacial describe la capacidad de diferenciar "
            "estructuras pequeñas y próximas."
        ),
    },

    {
        "tema": "Detectores",
        "pregunta": "¿Qué componente puede formar parte de un detector digital basado en TFT?",
        "opciones": [
            "Matriz de transistores de película delgada",
            "Filamento de tungsteno del tubo",
            "Ánodo rotatorio",
            "Colimador de plomo",
        ],
        "respuesta": "Matriz de transistores de película delgada",
        "explicacion": (
            "Los TFT pueden utilizarse como elementos de lectura en "
            "matrices de detectores digitales."
        ),
    },

    {
        "tema": "Detectores",
        "pregunta": "¿Qué factor influye en la calidad de una imagen digital?",
        "opciones": [
            "Resolución, contraste, ruido y características del detector",
            "Únicamente el color del equipo",
            "El tamaño de la sala",
            "La temperatura exterior exclusivamente",
        ],
        "respuesta": "Resolución, contraste, ruido y características del detector",
        "explicacion": (
            "La calidad de imagen depende de diferentes factores, entre ellos "
            "resolución, contraste, ruido y características del sistema detector."
        ),
    },


    # ========================================================
    # PROCESAMIENTO
    # ========================================================

    {
        "tema": "Procesamiento",
        "pregunta": "¿Qué permite modificar el ajuste de brillo de una imagen?",
        "opciones": [
            "Modificar globalmente los niveles de intensidad",
            "Cambiar el tamaño físico del paciente",
            "Cambiar la posición del detector",
            "Modificar el voltaje real del tubo después de adquirir la imagen",
        ],
        "respuesta": "Modificar globalmente los niveles de intensidad",
        "explicacion": (
            "El ajuste de brillo modifica los valores de intensidad de "
            "los píxeles para cambiar la apariencia de la imagen."
        ),
    },

    {
        "tema": "Procesamiento",
        "pregunta": "¿Qué ocurre al aumentar el contraste de una imagen?",
        "opciones": [
            "Se amplían las diferencias entre niveles de intensidad",
            "Todos los píxeles adquieren exactamente el mismo valor",
            "La imagen desaparece",
            "Se elimina automáticamente todo el ruido",
        ],
        "respuesta": "Se amplían las diferencias entre niveles de intensidad",
        "explicacion": (
            "El contraste representa las diferencias entre intensidades "
            "de la imagen y puede modificarse mediante procesamiento digital."
        ),
    },

    {
        "tema": "Procesamiento",
        "pregunta": "¿Para qué sirve un histograma de imagen?",
        "opciones": [
            "Para mostrar la distribución de intensidades de los píxeles",
            "Para medir directamente la presión arterial",
            "Para calcular la masa del paciente",
            "Para controlar la corriente del tubo",
        ],
        "respuesta": "Para mostrar la distribución de intensidades de los píxeles",
        "explicacion": (
            "El histograma muestra cuántos píxeles existen en diferentes "
            "niveles de intensidad."
        ),
    },

    {
        "tema": "Procesamiento",
        "pregunta": "¿Qué busca la ecualización de histograma?",
        "opciones": [
            "Redistribuir las intensidades para mejorar el contraste",
            "Eliminar todos los píxeles oscuros",
            "Convertir la imagen en sonido",
            "Cambiar físicamente la exposición realizada",
        ],
        "respuesta": "Redistribuir las intensidades para mejorar el contraste",
        "explicacion": (
            "La ecualización modifica la distribución de intensidades "
            "para mejorar determinadas características de contraste."
        ),
    },

    {
        "tema": "Procesamiento",
        "pregunta": "¿Qué característica tiene un filtro Gaussiano?",
        "opciones": [
            "Suaviza la imagen y puede reducir ruido de alta frecuencia",
            "Siempre aumenta el ruido",
            "Convierte una imagen en una señal de audio",
            "Elimina físicamente la radiación del paciente",
        ],
        "respuesta": "Suaviza la imagen y puede reducir ruido de alta frecuencia",
        "explicacion": (
            "El filtro Gaussiano realiza un suavizado que puede reducir "
            "variaciones rápidas asociadas al ruido."
        ),
    },

    {
        "tema": "Procesamiento",
        "pregunta": "¿Qué hace una corrección gamma?",
        "opciones": [
            "Modifica de forma no lineal la relación entre entrada y salida de intensidad",
            "Cambia el voltaje del tubo de Rayos X",
            "Cambia el material del detector",
            "Elimina automáticamente la radiación dispersa del paciente",
        ],
        "respuesta": "Modifica de forma no lineal la relación entre entrada y salida de intensidad",
        "explicacion": (
            "La transformación gamma permite modificar de manera no lineal "
            "la representación de las intensidades."
        ),
    },


    # ========================================================
    # ANÁLISIS
    # ========================================================

    {
        "tema": "Análisis",
        "pregunta": "¿Qué representa la media de intensidad de una imagen?",
        "opciones": [
            "El valor promedio de intensidad de sus píxeles",
            "El número total de imágenes guardadas",
            "La resolución espacial del detector",
            "El voltaje utilizado durante la adquisición",
        ],
        "respuesta": "El valor promedio de intensidad de sus píxeles",
        "explicacion": (
            "La media se obtiene calculando el promedio de los valores "
            "de intensidad de todos los píxeles."
        ),
    },

    {
        "tema": "Análisis",
        "pregunta": "¿Qué indica la desviación estándar de las intensidades?",
        "opciones": [
            "Cuánto se dispersan los valores respecto a la media",
            "La cantidad de Rayos X producidos por el tubo",
            "El tamaño físico del detector",
            "La velocidad de la radiografía",
        ],
        "respuesta": "Cuánto se dispersan los valores respecto a la media",
        "explicacion": (
            "La desviación estándar cuantifica la dispersión de los valores "
            "de intensidad alrededor de la media."
        ),
    },

    {
        "tema": "Análisis",
        "pregunta": "¿Qué permite comparar una imagen original con una procesada?",
        "opciones": [
            "Observar cómo cambió su distribución de intensidades y características",
            "Determinar automáticamente la edad del paciente",
            "Modificar el tubo de Rayos X",
            "Cambiar el detector físicamente",
        ],
        "respuesta": "Observar cómo cambió su distribución de intensidades y características",
        "explicacion": (
            "Comparar ambas imágenes permite estudiar los efectos del "
            "procesamiento sobre las intensidades y características visuales."
        ),
    },

    {
        "tema": "Análisis",
        "pregunta": "¿Qué información puede proporcionar un histograma durante el análisis?",
        "opciones": [
            "La distribución de niveles de intensidad",
            "La identidad del paciente",
            "La marca del tubo",
            "La temperatura del detector",
        ],
        "respuesta": "La distribución de niveles de intensidad",
        "explicacion": (
            "El histograma permite analizar cómo están distribuidos "
            "los niveles de intensidad de una imagen."
        ),
    },

    {
        "tema": "Análisis",
        "pregunta": "¿Qué significa comparar cuantitativamente dos imágenes?",
        "opciones": [
            "Evaluar mediante valores numéricos cómo difieren",
            "Mirarlas únicamente sin realizar ninguna medición",
            "Cambiar el voltaje del tubo",
            "Volver a realizar la radiografía",
        ],
        "respuesta": "Evaluar mediante valores numéricos cómo difieren",
        "explicacion": (
            "El análisis cuantitativo utiliza estadísticas y medidas "
            "numéricas para estudiar diferencias entre imágenes."
        ),
    },

    {
        "tema": "Análisis",
        "pregunta": "¿Qué puede indicar un cambio importante en el histograma después del procesamiento?",
        "opciones": [
            "Que cambió la distribución de intensidades de la imagen",
            "Que el paciente cambió físicamente",
            "Que el tubo dejó de funcionar",
            "Que la imagen necesariamente perdió toda su información",
        ],
        "respuesta": "Que cambió la distribución de intensidades de la imagen",
        "explicacion": (
            "Una modificación del histograma indica que el procesamiento "
            "alteró la distribución de los niveles de intensidad."
        ),
    },
]


# ============================================================
# CONFIGURACIÓN DE ACTIVIDADES
# ============================================================

NUMERO_PREGUNTAS = 10

TEMAS = [
    "Fundamentos",
    "Producción",
    "Formación",
    "Detectores",
    "Procesamiento",
    "Análisis",
]


# ============================================================
# UTILIDADES
# ============================================================

def obtener_ruta_resultados():
    """
    Devuelve la ruta oficial del archivo de resultados.
    """

    raiz = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    carpeta = os.path.join(
        raiz,
        "resultados"
    )

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    return os.path.join(
        carpeta,
        "resultados_estudiantes.csv"
    )


def generar_cuestionario():
    """
    Genera 10 preguntas diferentes utilizando
    todos los temas de manera equilibrada.

    Cada cuestionario tiene:
    - 10 preguntas
    - preguntas aleatorias
    - opciones aleatorias
    """

    preguntas_por_tema = {}

    for pregunta in BANCO_PREGUNTAS:
        tema = pregunta["tema"]

        if tema not in preguntas_por_tema:
            preguntas_por_tema[tema] = []

        preguntas_por_tema[tema].append(
            pregunta
        )

    # Elegimos aleatoriamente qué 4 temas tendrán 2 preguntas
    temas_dobles = random.sample(
        TEMAS,
        4
    )

    cuestionario = []

    for tema in TEMAS:

        cantidad = 2 if tema in temas_dobles else 1

        seleccionadas = random.sample(
            preguntas_por_tema[tema],
            cantidad
        )

        for pregunta in seleccionadas:

            opciones = list(
                pregunta["opciones"]
            )

            random.shuffle(
                opciones
            )

            nueva_pregunta = {
                "tema": pregunta["tema"],
                "pregunta": pregunta["pregunta"],
                "opciones": opciones,
                "respuesta": pregunta["respuesta"],
                "explicacion": pregunta["explicacion"],
            }

            cuestionario.append(
                nueva_pregunta
            )

    random.shuffle(
        cuestionario
    )

    return cuestionario


def guardar_resultado(
    nombre,
    puntaje
):
    """
    Guarda el resultado del estudiante
    en resultados/resultados_estudiantes.csv.
    """

    ruta = obtener_ruta_resultados()

    archivo_existe = os.path.exists(
        ruta
    )

    with open(
        ruta,
        "a",
        newline="",
        encoding="utf-8"
    ) as archivo:

        campos = [
            "nombre",
            "fecha",
            "actividad",
            "puntaje",
        ]

        escritor = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        if not archivo_existe:
            escritor.writeheader()

        escritor.writerow(
            {
                "nombre": nombre,
                "fecha": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "actividad": "Actividad Rayos X",
                "puntaje": round(
                    puntaje,
                    2
                ),
            }
        )


# ============================================================
# TARJETA DE PREGUNTA
# ============================================================

def crear_pregunta(
    pregunta,
    indice
):
    """
    Crea visualmente una pregunta.
    """

    opciones = [
        {
            "label": opcion,
            "value": opcion,
        }
        for opcion in pregunta["opciones"]
    ]

    return html.Div(
        [

            html.Div(
                [
                    html.Span(
                        f"{indice + 1:02d}",
                        style={
                            "fontSize": "12px",
                            "fontWeight": "800",
                            "color": THEME["cream"],
                            "backgroundColor": THEME["blue"],
                            "padding": "7px 10px",
                            "borderRadius": "7px",
                            "marginRight": "10px",
                        },
                    ),

                    html.Span(
                        pregunta["tema"].upper(),
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "1.5px",
                            "fontWeight": "700",
                            "color": THEME["beige"],
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "16px",
                },
            ),

            html.Div(
                pregunta["pregunta"],
                style={
                    "fontSize": "15px",
                    "fontWeight": "700",
                    "lineHeight": "1.55",
                    "color": THEME["text"],
                    "marginBottom": "18px",
                },
            ),

            dcc.RadioItems(
                id={
                    "type": "respuesta-actividad",
                    "index": indice,
                },
                options=opciones,
                value=None,
                labelStyle={
                    "display": "block",
                    "padding": "10px 12px",
                    "marginBottom": "8px",
                    "borderRadius": "8px",
                    "backgroundColor": THEME["bg_secondary"],
                    "color": THEME["text_secondary"],
                    "cursor": "pointer",
                },
                inputStyle={
                    "marginRight": "10px",
                },
            ),

        ],
        style={
            "backgroundColor": THEME["card"],
            "border": f"1px solid {THEME['border']}",
            "borderRadius": "13px",
            "padding": "22px",
            "marginBottom": "18px",
        },
    )


# ============================================================
# MOSTRAR ACTIVIDADES
# ============================================================

def mostrar_actividades():

    return html.Div(
        [

            # ------------------------------------------------
            # ENCABEZADO
            # ------------------------------------------------

            html.Div(
                [

                    html.Div(
                        "EVALUACIÓN INTERACTIVA",
                        style={
                            "fontSize": "10px",
                            "letterSpacing": "2px",
                            "fontWeight": "700",
                            "color": THEME["beige"],
                            "marginBottom": "10px",
                        },
                    ),

                    html.H1(
                        "📝 Actividades",
                        style={
                            "fontSize": "32px",
                            "fontWeight": "700",
                            "color": THEME["text"],
                            "margin": "0 0 12px 0",
                        },
                    ),

                    html.P(
                        "Comprueba cuánto aprendiste sobre Rayos X.",
                        style={
                            "fontSize": "15px",
                            "lineHeight": "1.6",
                            "color": THEME["text_secondary"],
                            "maxWidth": "760px",
                            "margin": "0",
                        },
                    ),

                ],
                style={
                    "marginBottom": "28px",
                },
            ),


            # ------------------------------------------------
            # IDENTIFICACIÓN
            # ------------------------------------------------

            html.Div(
                [

                    html.Div(
                        [
                            html.Div(
                                "👤 Nombre del estudiante",
                                style={
                                    "fontSize": "13px",
                                    "fontWeight": "700",
                                    "color": THEME["text"],
                                    "marginBottom": "8px",
                                },
                            ),

                            dcc.Input(
                                id="actividad-nombre",
                                type="text",
                                placeholder="Escribe tu nombre completo",
                                debounce=True,
                                style={
                                    "width": "100%",
                                    "padding": "12px 14px",
                                    "borderRadius": "8px",
                                    "border": f"1px solid {THEME['border']}",
                                    "backgroundColor": THEME["bg_secondary"],
                                    "color": THEME["text"],
                                    "boxSizing": "border-box",
                                    "fontSize": "13px",
                                },
                            ),
                        ],
                        style={
                            "flex": "1",
                        },
                    ),

                    html.Div(
                        [

                            html.Button(
                                "▶ Comenzar actividad",
                                id="btn-generar-actividad",
                                n_clicks=0,
                                style={
                                    "width": "100%",
                                    "padding": "12px 18px",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "backgroundColor": THEME["blue"],
                                    "color": THEME["cream"],
                                    "fontWeight": "700",
                                    "fontSize": "13px",
                                    "cursor": "pointer",
                                },
                            ),

                        ],
                        style={
                            "width": "220px",
                        },
                    ),

                ],
                style={
                    "display": "flex",
                    "gap": "18px",
                    "alignItems": "flex-end",
                    "backgroundColor": THEME["card"],
                    "border": f"1px solid {THEME['border']}",
                    "borderRadius": "13px",
                    "padding": "22px",
                    "marginBottom": "25px",
                },
            ),


            html.Div(
                id="actividad-mensaje",
                style={
                    "marginBottom": "15px",
                },
            ),


            # ------------------------------------------------
            # PREGUNTAS
            # ------------------------------------------------

            dcc.Store(
                id="actividades-preguntas",
                data=None,
            ),

            html.Div(
                id="actividad-preguntas",
            ),


            # ------------------------------------------------
            # BOTONES DE FINALIZACIÓN
            # ------------------------------------------------

            html.Div(
                [

                    html.Button(
                        "✓ Calificar actividad",
                        id="btn-calificar-actividad",
                        n_clicks=0,
                        style={
                            "padding": "13px 24px",
                            "border": "none",
                            "borderRadius": "8px",
                            "backgroundColor": THEME["beige"],
                            "color": THEME["bg"],
                            "fontWeight": "800",
                            "fontSize": "13px",
                            "cursor": "pointer",
                        },
                    ),

                    html.Button(
                        "↻ Nuevo cuestionario",
                        id="btn-nuevo-cuestionario",
                        n_clicks=0,
                        style={
                            "padding": "13px 24px",
                            "border": f"1px solid {THEME['border']}",
                            "borderRadius": "8px",
                            "backgroundColor": "transparent",
                            "color": THEME["cream"],
                            "fontWeight": "700",
                            "fontSize": "13px",
                            "cursor": "pointer",
                        },
                    ),

                ],
                style={
                    "display": "flex",
                    "gap": "12px",
                    "marginTop": "12px",
                    "marginBottom": "25px",
                },
            ),


            # ------------------------------------------------
            # RESULTADO
            # ------------------------------------------------

            html.Div(
                id="resultado-actividad",
            ),

        ],
        style={
            "width": "100%",
            "maxWidth": "1050px",
        },
    )


# ============================================================
# CALLBACKS
# ============================================================

def registrar_callbacks(app):

    # ========================================================
    # GENERAR CUESTIONARIO
    # ========================================================

    @app.callback(
        Output(
            "actividades-preguntas",
            "data"
        ),
        Output(
            "actividad-preguntas",
            "children"
        ),
        Output(
            "actividad-mensaje",
            "children"
        ),
        Input(
            "btn-generar-actividad",
            "n_clicks"
        ),
        Input(
            "btn-nuevo-cuestionario",
            "n_clicks"
        ),
        State(
            "actividad-nombre",
            "value"
        ),
        prevent_initial_call=True,
    )
    def generar_actividad(
        clicks_inicio,
        clicks_nuevo,
        nombre
    ):

        if not nombre or not nombre.strip():

            mensaje = html.Div(
                "⚠️ Escribe tu nombre antes de comenzar.",
                style={
                    "color": THEME["error"],
                    "fontSize": "13px",
                    "fontWeight": "700",
                    "padding": "10px 0",
                },
            )

            return (
                no_update,
                no_update,
                mensaje,
            )

        cuestionario = generar_cuestionario()

        preguntas = []

        for indice, pregunta in enumerate(
            cuestionario
        ):

            preguntas.append(
                {
                    "indice": indice,
                    "tema": pregunta["tema"],
                    "pregunta": pregunta["pregunta"],
                    "opciones": pregunta["opciones"],
                    "respuesta": pregunta["respuesta"],
                    "explicacion": pregunta["explicacion"],
                }
            )

        children = [
            crear_pregunta(
                pregunta,
                indice
            )
            for indice, pregunta in enumerate(
                preguntas
            )
        ]

        mensaje = html.Div(
            [
                html.Span(
                    "✓ Cuestionario generado. ",
                    style={
                        "fontWeight": "800",
                        "color": THEME["success"],
                    },
                ),

                html.Span(
                    "Tienes 10 preguntas diferentes para este intento.",
                    style={
                        "color": THEME["text_secondary"],
                    },
                ),
            ],
            style={
                "fontSize": "13px",
                "padding": "10px 0",
            },
        )

        return (
            preguntas,
            children,
            mensaje,
        )


    # ========================================================
    # CALIFICAR ACTIVIDAD
    # ========================================================

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
            "actividades-preguntas",
            "data"
        ),
        State(
            "actividad-nombre",
            "value"
        ),
        State(
            {
                "type": "respuesta-actividad",
                "index": ALL,
            },
            "value"
        ),
        prevent_initial_call=True,
    )
    def calificar_actividad(
        n_clicks,
        preguntas,
        nombre,
        respuestas
    ):

        if not n_clicks:
            return no_update

        if not preguntas:

            return html.Div(
                "⚠️ Primero debes comenzar una actividad.",
                style={
                    "color": THEME["error"],
                    "fontWeight": "700",
                    "padding": "15px 0",
                },
            )

        if not nombre or not nombre.strip():

            return html.Div(
                "⚠️ Escribe tu nombre antes de calificar.",
                style={
                    "color": THEME["error"],
                    "fontWeight": "700",
                    "padding": "15px 0",
                },
            )

        respuestas = respuestas or []

        puntaje = 0
        correctas = 0
        sin_responder = 0

        resultados = []

        for indice, pregunta in enumerate(
            preguntas
        ):

            respuesta_usuario = (
                respuestas[indice]
                if indice < len(respuestas)
                else None
            )

            respuesta_correcta = pregunta[
                "respuesta"
            ]

            es_correcta = (
                respuesta_usuario
                == respuesta_correcta
            )

            if es_correcta:
                puntaje += 1
                correctas += 1

            if respuesta_usuario is None:
                sin_responder += 1

            resultados.append(
                {
                    "numero": indice + 1,
                    "pregunta": pregunta["pregunta"],
                    "usuario": respuesta_usuario,
                    "correcta": respuesta_correcta,
                    "es_correcta": es_correcta,
                    "explicacion": pregunta["explicacion"],
                }
            )

        porcentaje = (
            puntaje / len(preguntas)
        ) * 100

        guardar_resultado(
            nombre.strip(),
            puntaje
        )

        # ====================================================
        # ENCABEZADO DEL RESULTADO
        # ====================================================

        tarjeta_resultado = html.Div(
            [

                html.Div(
                    "RESULTADO",
                    style={
                        "fontSize": "10px",
                        "letterSpacing": "2px",
                        "fontWeight": "800",
                        "color": THEME["beige"],
                        "marginBottom": "8px",
                    },
                ),

                html.Div(
                    f"{puntaje} / {len(preguntas)}",
                    style={
                        "fontSize": "42px",
                        "fontWeight": "800",
                        "color": THEME["cream"],
                        "lineHeight": "1",
                    },
                ),

                html.Div(
                    f"{porcentaje:.0f} %",
                    style={
                        "fontSize": "18px",
                        "fontWeight": "700",
                        "color": THEME["beige"],
                        "marginTop": "8px",
                    },
                ),

                html.P(
                    (
                        f"Excelente trabajo, {nombre.strip()}."
                        if porcentaje >= 80
                        else
                        f"Buen trabajo, {nombre.strip()}. "
                        "Revisa las explicaciones para seguir aprendiendo."
                    ),
                    style={
                        "fontSize": "13px",
                        "color": THEME["text_secondary"],
                        "margin": "12px 0 0 0",
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            f"✓ Correctas: {correctas}",
                            style={
                                "color": THEME["success"],
                                "fontWeight": "700",
                            },
                        ),

                        html.Div(
                            f"○ Sin responder: {sin_responder}",
                            style={
                                "color": THEME["beige"],
                                "fontWeight": "700",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "25px",
                        "marginTop": "16px",
                        "fontSize": "12px",
                    },
                ),

            ],
            style={
                "backgroundColor": THEME["card"],
                "border": f"1px solid {THEME['border']}",
                "borderLeft": f"4px solid {THEME['beige']}",
                "borderRadius": "13px",
                "padding": "24px",
                "marginBottom": "22px",
            },
        )


        # ====================================================
        # RETROALIMENTACIÓN
        # ====================================================

        tarjetas_feedback = []

        for resultado in resultados:

            if resultado["es_correcta"]:

                color = THEME["success"]
                icono = "✓"
                mensaje = "Respuesta correcta"

            elif resultado["usuario"] is None:

                color = THEME["beige"]
                icono = "○"
                mensaje = "Sin responder"

            else:

                color = THEME["error"]
                icono = "✕"
                mensaje = "Respuesta incorrecta"

            respuesta_usuario = (
                resultado["usuario"]
                if resultado["usuario"] is not None
                else "Sin respuesta"
            )

            tarjetas_feedback.append(
                html.Div(
                    [

                        html.Div(
                            [
                                html.Span(
                                    f"{icono} {resultado['numero']:02d}",
                                    style={
                                        "fontWeight": "800",
                                        "color": color,
                                        "marginRight": "10px",
                                    },
                                ),

                                html.Span(
                                    mensaje,
                                    style={
                                        "fontSize": "11px",
                                        "fontWeight": "700",
                                        "color": color,
                                    },
                                ),
                            ],
                            style={
                                "marginBottom": "10px",
                            },
                        ),

                        html.Div(
                            resultado["pregunta"],
                            style={
                                "fontSize": "13px",
                                "fontWeight": "700",
                                "color": THEME["text"],
                                "lineHeight": "1.5",
                                "marginBottom": "10px",
                            },
                        ),

                        html.Div(
                            [
                                html.Strong(
                                    "Tu respuesta: "
                                ),
                                respuesta_usuario,
                            ],
                            style={
                                "fontSize": "12px",
                                "color": THEME["text_secondary"],
                                "marginBottom": "5px",
                            },
                        ),

                        html.Div(
                            [
                                html.Strong(
                                    "Respuesta correcta: "
                                ),
                                resultado["correcta"],
                            ],
                            style={
                                "fontSize": "12px",
                                "color": THEME["cream"],
                                "marginBottom": "8px",
                            },
                        ),

                        html.Div(
                            [
                                html.Strong(
                                    "💡 Explicación: "
                                ),
                                resultado["explicacion"],
                            ],
                            style={
                                "fontSize": "12px",
                                "lineHeight": "1.6",
                                "color": THEME["text_secondary"],
                            },
                        ),

                    ],
                    style={
                        "backgroundColor": THEME["bg_secondary"],
                        "border": f"1px solid {THEME['border']}",
                        "borderRadius": "11px",
                        "padding": "18px",
                        "marginBottom": "12px",
                    },
                )
            )


        return html.Div(
            [
                tarjeta_resultado,

                html.H3(
                    "📚 Revisión de respuestas",
                    style={
                        "fontSize": "18px",
                        "color": THEME["text"],
                        "marginBottom": "15px",
                    },
                ),

                html.Div(
                    tarjetas_feedback
                ),
            ]
        )
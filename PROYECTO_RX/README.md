PLATAFORMA EDUCATIVA DE RAYOS X

1. Descripción del proyecto

La Plataforma Educativa de Rayos X es una aplicación interactiva desarrollada en Python utilizando Dash y Plotly. Su finalidad es facilitar el aprendizaje de los principales conceptos relacionados con la producción, interacción, formación y análisis de imágenes obtenidas mediante Rayos X.

La plataforma integra contenidos teóricos, elementos visuales, procesamiento de imágenes, análisis y un asistente educativo basado en Gemini.

El recorrido educativo comprende:

Rayos X → Física → Producción → Interacción → Atenuación → Formación de imagen → Detectores → Radiografía digital → Procesamiento → Análisis → Base de conocimiento → Gemini → Actividades educativas.

2. Objetivo

Desarrollar una plataforma educativa interactiva que permita comprender de manera visual y práctica los fundamentos de los Rayos X y su aplicación en la formación, procesamiento y análisis de imágenes radiográficas.

3. Requisitos

Para ejecutar el proyecto se requiere:

Python 3.10 o superior.

Dash.

Plotly.

NumPy.

SciPy.

Scikit-image.

Pillow.

Python-dotenv.

Google Generative AI.

Las dependencias se encuentran registradas en requirements.txt.

4. Instalación

Windows

Crear un entorno virtual:

python -m venv venv

Activar el entorno virtual:

venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

Linux / macOS

Crear el entorno virtual:

python3 -m venv venv

Activarlo:

source venv/bin/activate

Instalar las dependencias:

pip install -r requirements.txt

5. Ejecución

Para ejecutar la plataforma:

python main.py

Luego abrir en el navegador:

http://127.0.0.1:8050/

6. Estructura del proyecto

PROYECTO_RX/
├── main.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── modulos/
│   ├── __init__.py
│   ├── interfaz.py
│   ├── teoria_rx.py
│   ├── formacion_imagen.py
│   ├── procesamiento.py
│   ├── analisis.py
│   └── gemini_rx.py
├── dataset_rx/
│   ├── fundamentos.txt
│   ├── produccion_rx.txt
│   ├── atenuacion_rx.txt
│   ├── formacion_imagen.txt
│   ├── detectores.txt
│   ├── radiografia_digital.txt
│   ├── procesamiento_rx.txt
│   └── seguridad_radiologica.txt
├── assets/
│   ├── interfaz/
│   ├── teoria/
│   └── formacion/
├── imagenes_rx/
│   ├── originales/
│   └── procesadas/
├── resultados/
│   └── resultados_estudiantes.csv
└── pruebas/
    ├── prueba_procesamiento.py
    ├── prueba_analisis.py
    └── prueba_gemini.py

7. Uso de la plataforma

Inicio

La página principal presenta la plataforma y permite acceder a los diferentes módulos educativos.

Fundamentos de Rayos X

Contiene los conceptos fundamentales relacionados con los Rayos X, su naturaleza física y los principios necesarios para comprender su utilización en radiología.

Producción de Rayos X

Presenta los principios relacionados con la generación de Rayos X y los componentes involucrados en este proceso.

Formación de imagen

Explica cómo los Rayos X interactúan con el objeto y cómo estas interacciones permiten generar una imagen radiográfica.

Detectores

Presenta los principales conceptos relacionados con la detección de la radiación y la obtención de imágenes digitales.

Procesamiento

Permite trabajar con imágenes radiográficas y aplicar diferentes técnicas de procesamiento digital.

Análisis

Permite realizar análisis sobre las imágenes y obtener información útil para el aprendizaje.

Asistente Gemini

Integra un asistente educativo basado en Gemini para responder preguntas relacionadas con los contenidos de Rayos X.

Actividades

Contiene actividades educativas orientadas a reforzar los conocimientos adquiridos durante el recorrido de la plataforma.

8. Uso de Gemini

El módulo modulos/gemini_rx.py está destinado a la integración de un asistente educativo basado en Gemini.

La configuración de la API se realizará mediante el archivo .env.

La clave de API debe mantenerse privada y no debe compartirse ni subirse al repositorio.

9. Dataset

El directorio dataset_rx/ contiene información relacionada con los diferentes temas educativos de la plataforma.

Los contenidos incluyen:

Fundamentos.

Producción de Rayos X.

Atenuación.

Formación de imagen.

Detectores.

Radiografía digital.

Procesamiento.

Seguridad radiológica.

10. Procesamiento de imágenes

Las imágenes utilizadas en el proyecto se organizan en:

imagenes_rx/
├── originales/
└── procesadas/

Las imágenes originales corresponden a los archivos utilizados como entrada.

Las imágenes procesadas corresponden a los resultados obtenidos después de aplicar técnicas de procesamiento digital.

Para estas funciones se utilizan bibliotecas como NumPy, SciPy, Scikit-image y Pillow.

11. Arquitectura del proyecto

El archivo principal es main.py, encargado de crear y ejecutar la aplicación Dash.

La interfaz principal se encuentra en modulos/interfaz.py.

Los módulos educativos se distribuyen de la siguiente manera:

Módulo

Archivo

Fundamentos y teoría

modulos/teoria_rx.py

Formación de imagen

modulos/formacion_imagen.py

Procesamiento

modulos/procesamiento.py

Análisis

modulos/analisis.py

Asistente Gemini

modulos/gemini_rx.py

12. Desarrollo colaborativo

El proyecto se desarrolla de manera colaborativa, distribuyendo los módulos entre los integrantes del grupo.

Cada integrante trabaja principalmente sobre los archivos asignados y posteriormente los módulos son integrados en la aplicación principal.

La integración final debe mantener la estructura establecida para el proyecto y evitar modificaciones innecesarias de archivos o carpetas.

13. Pruebas

El proyecto dispone de un directorio pruebas/ donde se encuentran las pruebas correspondientes a los módulos de procesamiento, análisis y Gemini.

Las pruebas permiten verificar individualmente el funcionamiento de los componentes antes de realizar la integración completa.

14. Tecnologías utilizadas

Las principales tecnologías utilizadas son:

Python.

Dash.

Plotly.

NumPy.

SciPy.

Scikit-image.

Pillow.

Google Generative AI.

Dash se utiliza para desarrollar la interfaz web interactiva.

Plotly se utiliza para la representación gráfica y visualización de datos.

Las bibliotecas de procesamiento permiten trabajar con imágenes radiográficas digitales.

Gemini se utiliza como asistente educativo.

15. Consideraciones de uso

La plataforma tiene finalidad educativa.

Los contenidos y herramientas proporcionados están destinados al aprendizaje de los principios relacionados con los Rayos X, la formación de imágenes, el procesamiento digital y su análisis.

El asistente Gemini debe utilizarse como apoyo educativo y no como sustituto de la evaluación o criterio profesional.

16. Estado del proyecto

El proyecto se encuentra en desarrollo e integración.

La implementación se realiza progresivamente mediante módulos independientes que posteriormente serán integrados en una única plataforma educativa.

El objetivo final es disponer de una aplicación interactiva que combine teoría, visualización, procesamiento de imágenes, análisis, actividades educativas y asistencia mediante inteligencia artificial.
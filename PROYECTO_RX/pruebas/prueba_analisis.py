# ============================================================
# PRUEBA DEL MODULO DE ANALISIS DE IMAGENES RX
# Integrante 5
# ============================================================

import numpy as np

from modulos.analisis import (
    calcular_estadisticas,
    calcular_contraste,
    comparar_imagenes,
    generar_reporte,
    corregir_actividad,
    guardar_resultado_actividad,
    mostrar_analisis,
)


def ejecutar_prueba(nombre, funcion):
    try:
        funcion()
        print(f"[OK] {nombre}")
        return True

    except Exception as error:
        print(f"[ERROR] {nombre}")
        print(f"       {error}")
        return False


def main():

    print("=" * 55)
    print(" PRUEBA DEL MODULO DE ANALISIS RX")
    print("=" * 55)

    # --------------------------------------------------------
    # Crear imágenes de prueba
    # --------------------------------------------------------

    imagen_original = np.array(
        [
            [0, 50, 100, 150],
            [50, 100, 150, 200],
            [100, 150, 200, 250],
            [150, 200, 250, 255]
        ],
        dtype=np.uint8
    )

    imagen_procesada = np.array(
        [
            [10, 60, 110, 160],
            [60, 110, 160, 210],
            [110, 160, 210, 250],
            [160, 210, 250, 255]
        ],
        dtype=np.uint8
    )

    resultados = []

    # --------------------------------------------------------
    # 1. Estadísticas
    # --------------------------------------------------------

    resultados.append(
        ejecutar_prueba(
            "Cálculo de estadísticas",
            lambda: calcular_estadisticas(
                imagen_original
            )
        )
    )

    # --------------------------------------------------------
    # 2. Contraste
    # --------------------------------------------------------

    resultados.append(
        ejecutar_prueba(
            "Cálculo de contraste",
            lambda: calcular_contraste(
                imagen_original
            )
        )
    )

    # --------------------------------------------------------
    # 3. Comparación
    # --------------------------------------------------------

    resultados.append(
        ejecutar_prueba(
            "Comparación de imágenes",
            lambda: comparar_imagenes(
                imagen_original,
                imagen_procesada
            )
        )
    )

    # --------------------------------------------------------
    # 4. Generación de reporte
    # --------------------------------------------------------

    resultados.append(
        ejecutar_prueba(
            "Generación de reporte",
            lambda: generar_reporte(
                imagen_original,
                imagen_procesada
            )
        )
    )

    # --------------------------------------------------------
    # 5. Corrección de actividad
    # --------------------------------------------------------

    respuestas = [
        1,
        2,
        1,
        2,
        0,
        1,
        0,
        0
    ]

    resultados.append(
        ejecutar_prueba(
            "Corrección de actividad",
            lambda: corregir_actividad(
                respuestas
            )
        )
    )

    # --------------------------------------------------------
    # 6. Interfaz de análisis
    # --------------------------------------------------------

    resultados.append(
        ejecutar_prueba(
            "Función mostrar_analisis()",
            lambda: mostrar_analisis()
        )
    )

    # --------------------------------------------------------
    # 7. Guardado de resultado
    # --------------------------------------------------------

    resultados.append(
        ejecutar_prueba(
            "Guardado de resultado en CSV",
            lambda: guardar_resultado_actividad(
                "Prueba",
                100
            )
        )
    )

    # --------------------------------------------------------
    # Resultado final
    # --------------------------------------------------------

    print()
    print("=" * 55)

    if all(resultados):

        print(" TODAS LAS PRUEBAS FUERON APROBADAS")
        print("=" * 55)

    else:

        print(" ALGUNAS PRUEBAS PRESENTARON ERRORES")
        print("=" * 55)


if __name__ == "__main__":
    main()
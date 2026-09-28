# ============================================================
# PRUEBA DEL MODULO DE PROCESAMIENTO DE IMAGENES RX
# Integrante 4
# ============================================================

import numpy as np

from modulos.procesamiento import (
    convertir_grises,
    ajustar_brillo,
    ajustar_contraste,
    aplicar_brillo_y_contraste,
    ecualizar_histograma,
    ecualizar_clahe,
    aplicar_gamma,
    aplicar_filtro,
    calcular_histograma,
    mostrar_procesamiento,
)


def ejecutar_prueba(nombre, funcion):
    """
    Ejecuta una prueba individual y muestra su resultado.
    """
    try:
        funcion()
        print(f"[OK] {nombre}")
    except Exception as error:
        print(f"[ERROR] {nombre}")
        print(f"       {error}")
        return False

    return True


def main():

    print("=" * 50)
    print(" PRUEBA DEL MODULO DE PROCESAMIENTO RX")
    print("=" * 50)

    # --------------------------------------------------------
    # Imagen de prueba
    # --------------------------------------------------------
    imagen = np.random.randint(
        0,
        256,
        (256, 256),
        dtype=np.uint8
    )

    resultados = []

    # --------------------------------------------------------
    # 1. Conversion a escala de grises
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Conversion a escala de grises",
            lambda: convertir_grises(imagen)
        )
    )

    # --------------------------------------------------------
    # 2. Ajuste de brillo
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Ajuste de brillo",
            lambda: ajustar_brillo(imagen, 30)
        )
    )

    # --------------------------------------------------------
    # 3. Ajuste de contraste
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Ajuste de contraste",
            lambda: ajustar_contraste(imagen, 1.5)
        )
    )

    # --------------------------------------------------------
    # 4. Brillo + contraste
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Brillo y contraste",
            lambda: aplicar_brillo_y_contraste(
                imagen,
                20,
                1.3
            )
        )
    )

    # --------------------------------------------------------
    # 5. Ecualizacion de histograma
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Ecualizacion de histograma",
            lambda: ecualizar_histograma(imagen)
        )
    )

    # --------------------------------------------------------
    # 6. CLAHE
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Ecualizacion CLAHE",
            lambda: ecualizar_clahe(imagen)
        )
    )

    # --------------------------------------------------------
    # 7. Gamma
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Correccion Gamma",
            lambda: aplicar_gamma(imagen, 1.2)
        )
    )

    # --------------------------------------------------------
    # 8. Filtro gaussiano
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Filtro Gaussiano",
            lambda: aplicar_filtro(
                imagen,
                "Gaussiano",
                5
            )
        )
    )

    # --------------------------------------------------------
    # 9. Filtro mediana
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Filtro de Mediana",
            lambda: aplicar_filtro(
                imagen,
                "Mediana",
                5
            )
        )
    )

    # --------------------------------------------------------
    # 10. Filtro bilateral
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Filtro Bilateral",
            lambda: aplicar_filtro(
                imagen,
                "Bilateral",
                5
            )
        )
    )

    # --------------------------------------------------------
    # 11. Filtro Sobel
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Filtro Sobel",
            lambda: aplicar_filtro(
                imagen,
                "Sobel",
                5
            )
        )
    )

    # --------------------------------------------------------
    # 12. Histograma
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Calculo de histograma",
            lambda: calcular_histograma(imagen)
        )
    )

    # --------------------------------------------------------
    # 13. Interfaz
    # --------------------------------------------------------
    resultados.append(
        ejecutar_prueba(
            "Funcion mostrar_procesamiento()",
            lambda: mostrar_procesamiento()
        )
    )

    # --------------------------------------------------------
    # Resultado final
    # --------------------------------------------------------
    print()
    print("=" * 50)

    if all(resultados):
        print(" TODAS LAS PRUEBAS FUERON APROBADAS")
        print("=" * 50)
    else:
        print(" ALGUNAS PRUEBAS PRESENTARON ERRORES")
        print("=" * 50)


if __name__ == "__main__":
    main()
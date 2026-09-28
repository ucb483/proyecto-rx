# ============================================================
# PRUEBA DEL MODULO GEMINI RX
# Integrante 5
# ============================================================

from modulos.gemini_rx import (
    cargar_contexto_dataset,
    consultar_gemini_con_contexto
)


def main():

    print("=" * 55)
    print(" PRUEBA DEL MODULO GEMINI RX")
    print("=" * 55)

    pruebas_correctas = True

    # --------------------------------------------------------
    # 1. Probar carga del dataset
    # --------------------------------------------------------

    print()
    print("1. Probando carga del dataset...")

    try:

        contexto = cargar_contexto_dataset()

        if contexto:

            print("[OK] Dataset cargado correctamente")
            print(
                f"     Caracteres cargados: {len(contexto)}"
            )

        else:

            print("[ERROR] No se pudo cargar el dataset")
            pruebas_correctas = False

    except Exception as error:

        print("[ERROR] Error al cargar el dataset")
        print(f"        {error}")
        pruebas_correctas = False

    # --------------------------------------------------------
    # 2. Probar consulta a Gemini
    # --------------------------------------------------------

    print()
    print("2. Probando consulta a Gemini...")

    pregunta = "¿Qué son los rayos X?"

    print(f"   Pregunta: {pregunta}")

    try:

        respuesta = consultar_gemini_con_contexto(
            pregunta
        )

        if respuesta:

            print("[OK] Gemini respondió correctamente")

            print()
            print("   Respuesta:")
            print("   " + respuesta.replace("\n", "\n   "))

        else:

            print("[ERROR] Gemini no devolvió respuesta")
            pruebas_correctas = False

    except Exception as error:

        print("[ERROR] No se pudo consultar Gemini")
        print(f"        {error}")
        pruebas_correctas = False

    # --------------------------------------------------------
    # Resultado final
    # --------------------------------------------------------

    print()
    print("=" * 55)

    if pruebas_correctas:

        print(" TODAS LAS PRUEBAS DE GEMINI FUERON APROBADAS")

    else:

        print(" ALGUNAS PRUEBAS DE GEMINI PRESENTARON ERRORES")

    print("=" * 55)


if __name__ == "__main__":
    main()
from funciones import (
    leer_api_key,
    obtener_argumentos,
    consultar_brechas,
    consultar_detalle_brecha,
    generar_csv
)
import logging

def main():
    """
    Bloque principal del programa.
    """
    try:
        api_key = leer_api_key()
        correo = obtener_argumentos()
        brechas = consultar_brechas(api_key, correo)

        if brechas is None:
            print("Ocurrió un error al consultar las brechas.")
            return

        for brecha in brechas:
            detalle = consultar_detalle_brecha(api_key, brecha["Name"])
            if detalle:
                brecha.update(detalle)

        generar_csv(correo, brechas)
        print("Consulta completada. Revisa el archivo reporte.csv y registro.log")

    except Exception as e:
        logging.error(f"Error general: {e}")
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
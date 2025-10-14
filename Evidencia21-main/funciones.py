import argparse
import csv
import logging
import os
import requests
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    filename='registro.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# FUNCIÓN: LECTURA SEGURA DE API KEY
def leer_api_key():
    """
    Lee la API key desde una variable de entorno para mayor seguridad.
    """
    api_key = os.getenv("HIBP_API_KEY")
    if not api_key:
        logging.error("No se encontró la variable de entorno HIBP_API_KEY.")
        raise ValueError("Error: No se encontró la API key.")
    return api_key

# FUNCIÓN: ARGUMENTOS CON ARGPARSE
def obtener_argumentos():
    """
    Obtiene el correo electrónico desde los argumentos de línea de comandos.
    """
    parser = argparse.ArgumentParser(description="Verifica si un correo ha sido filtrado en alguna brecha.")
    parser.add_argument("correo", type=str, help="Correo electrónico a verificar")
    args = parser.parse_args()
    return args.correo

# FUNCIÓN: CONSULTAR BRECHAS POR CORREO
def consultar_brechas(api_key, correo):
    """
    Consulta las brechas de datos en las que aparece el correo dado.
    """
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}"
    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "VerificadorDeBrechasApp"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            logging.info(f"Consulta exitosa para {correo}")
            return response.json()
        elif response.status_code == 404:
            logging.info(f"No se encontraron brechas para {correo}")
            return []
        else:
            logging.error(f"Error {response.status_code} en la consulta: {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"Error de conexión: {e}")
        return None

# FUNCIÓN: CONSULTAR DETALLES POR BRECHA
def consultar_detalle_brecha(api_key, nombre_brecha):
    """
    Obtiene detalles de una brecha específica.
    """
    url = f"https://haveibeenpwned.com/api/v3/breach/{nombre_brecha}"
    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "VerificadorDeBrechasApp"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"No se pudo obtener detalle para {nombre_brecha}")
            return None
    except requests.RequestException as e:
        logging.error(f"Error de conexión: {e}")
        return None

# FUNCIÓN: GENERAR ARCHIVO CSV
def generar_csv(correo, brechas):
    """
    Crea un archivo CSV con los resultados de la consulta.
    """
    with open("reporte.csv", mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Correo", "Nombre de la Brecha", "Dominio", "Fecha", "Descripción"])

        if not brechas:
            escritor.writerow([correo, "Sin brechas", "", "", ""])
            return

        for brecha in brechas:
            escritor.writerow([
                correo,
                brecha.get("Name", ""),
                brecha.get("Domain", ""),
                brecha.get("BreachDate", ""),
                brecha.get("Description", "").replace("\n", " ")
            ])
    logging.info(f"Archivo reporte.csv generado correctamente.")
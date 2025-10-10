import sys
import requests
import time
import getpass
import os
import csv
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Verificar argumento
if len(sys.argv) != 2:
    print("Uso: python verificar_correo.py correo@example.com")
    sys.exit(1)

correo = sys.argv[1]

# Lectura segura de API key
if not os.path.exists("apikey.txt"):
    print("🔐 No se encontró el archivo apikey.txt.")
    clave = getpass.getpass("Ingresa tu API key: ")
    with open("apikey.txt", "w") as archivo:
        archivo.write(clave.strip())

# Cargar API key
try:
    with open("apikey.txt", "r") as archivo:
        api_key = archivo.read().strip()
except Exception as e:
    print("❌ No se pudo leer la API key.")
    logging.error(f"Error leyendo apikey.txt: {e}")
    sys.exit(1)

# URL principal
url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}"
headers = {
    "hibp-api-key": api_key,
    "user-agent": "PythonScript"
}

# Hacer petición principal
try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        brechas = response.json()
        logging.info(f"Consulta exitosa para {correo}. Brechas encontradas: {len(brechas)}")

        # Crear y abrir el archivo reporte.csv
        with open("reporte.csv", "w", newline='', encoding="utf-8") as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow([
                "Título", "Dominio", "Fecha de Brecha",
                "Datos Comprometidos", "Verificada", "Sensible"
            ])

            # Escribir detalles de las primeras 3 brechas
            for i, brecha in enumerate(brechas[:3]):
                nombre = brecha["Name"]
                detalle_url = f"https://haveibeenpwned.com/api/v3/breach/{nombre}"
                detalle_resp = requests.get(detalle_url, headers=headers)

                if detalle_resp.status_code == 200:
                    detalle = detalle_resp.json()
                    writer.writerow([
                        detalle.get("Title"),
                        detalle.get("Domain"),
                        detalle.get("BreachDate"),
                        ", ".join(detalle.get("DataClasses", [])),
                        detalle.get("IsVerified"),
                        detalle.get("IsSensitive")
                    ])
                else:
                    logging.error(f"No se pudo obtener detalles de la brecha: {nombre}")

                if i < 2:
                    print("⏳ Esperando 10 segundos para la siguiente brecha...")
                    time.sleep(10)

        print(f"✅ Reporte generado en 'reporte.csv' para el correo {correo}.")

    elif response.status_code == 404:
        print(f"✔️ La cuenta {correo} no aparece en ninguna brecha conocida.")
        logging.info(f"Consulta exitosa para {correo}. No se encontraron brechas.")
    elif response.status_code == 401:
        print("❌ Error de autenticación: revisa tu API key.")
        logging.error("Error 401: API key inválida.")
    else:
        print(f"❌ Error inesperado. Código de estado: {response.status_code}")
        logging.error(f"Error inesperado. Código de estado: {response.status_code}")

except Exception as e:
    print(f"❌ Error durante la consulta: {e}")
    logging.error(f"Excepción no controlada: {e}")

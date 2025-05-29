import requests
from datetime import datetime
import csv
import os
from alertas import enviar_alerta
from colorama import init, Fore, Style

init(autoreset=True)  # Inicializa colorama para resetear colores automáticamente

def cargar_urls(archivo="urls.txt"):
    with open(archivo, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def verificar_url(url):
    try:
        respuesta = requests.get(url, timeout=5)
        estado = "UP" if respuesta.status_code == 200 else f"DOWN ({respuesta.status_code})"
        tiempo = round(respuesta.elapsed.total_seconds(), 2)
    except requests.exceptions.RequestException:
        estado = "DOWN (Error)"
        tiempo = None
    return {
        "url": url,
        "estado": estado,
        "tiempo": tiempo,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def guardar_resultado_csv(resultado, archivo="resultados.csv"):
    archivo_existe = os.path.isfile(archivo)
    with open(archivo, mode="a", newline="", encoding="utf-8") as f:
        campos = ["timestamp", "url", "estado", "tiempo"]
        escritor = csv.DictWriter(f, fieldnames=campos)
        if not archivo_existe:
            escritor.writeheader()
        escritor.writerow({
            "timestamp": resultado["timestamp"],
            "url": resultado["url"],
            "estado": resultado["estado"],
            "tiempo": resultado["tiempo"] if resultado["tiempo"] is not None else "N/A"
        })

def monitorear():
    urls = cargar_urls()
    print("=" * 50)
    print(f"🕒 Revisión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for url in urls:
        resultado = verificar_url(url)
        
        if "DOWN" in resultado["estado"]:
            # Alerta visual en rojo
            print(Fore.RED + f"[{resultado['timestamp']}] {resultado['url']} ➤ {resultado['estado']} | Tiempo: {resultado['tiempo']}s" + Style.RESET_ALL)
            
            # Envío de correo
            enviar_alerta("andress.romero.2004@gmail.com", resultado["url"])  # Cambia por tu correo real

        else:
            print(f"[{resultado['timestamp']}] {resultado['url']} ➤ {resultado['estado']} | Tiempo: {resultado['tiempo']}s")

        guardar_resultado_csv(resultado)

import schedule
import time
from monitor import monitorear

# Programar la tarea cada 5 minutos
schedule.every(5).minutes.do(monitorear)

print("🔍 Monitor de sitios iniciado. Presiona Ctrl+C para detener.")

# Ejecutar por primera vez inmediatamente
monitorear()

# Bucle principal
while True:
    schedule.run_pending()
    time.sleep(1)

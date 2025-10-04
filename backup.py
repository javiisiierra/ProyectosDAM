import subprocess
from datetime import datetime
import os

# Obtener ruta actual (ProyectosDAM)
ruta_repo = os.getcwd()

print(f"[{datetime.now()}] Iniciando copia de seguridad a GitHub en: {ruta_repo}")

try:
    subprocess.run(["git", "add", "."], check=True)

    mensaje = f"Backup automático - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    result = subprocess.run(["git", "commit", "-m", mensaje], capture_output=True, text=True)

    if "nothing to commit" in result.stdout:
        print(f"[{datetime.now()}] No hay cambios nuevos para hacer commit.")
    else:
        print(f"[{datetime.now()}] Commit realizado correctamente.")

        subprocess.run(["git", "push"], check=True)
        print(f"[{datetime.now()}] Push a GitHub realizado con éxito.")

except subprocess.CalledProcessError as e:
    print(f"[{datetime.now()}] Error al ejecutar git: {e}")


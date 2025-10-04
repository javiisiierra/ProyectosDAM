import os
import shutil
from datetime import datetime
import subprocess
from pathlib import Path
import filecmp

# CONFIGURACIÓN
CARPETA_ORIGEN = Path(__file__).parent  # ProyectosDAM
CARPETA_DESTINO_NAS = Path(r'C:\Users\usuario\Desktop\BackupsDAM')  # <-- CAMBIA ESTA RUTA si usas otra
COMMIT_MENSAJE = f"Backup automático {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# FUNCIÓN: Backup a GitHub
def backup_github():
    print(f"[{datetime.now()}] Iniciando copia de seguridad a GitHub en: {CARPETA_ORIGEN}")

    try:
        subprocess.run(["git", "add", "."], cwd=CARPETA_ORIGEN, check=True)
        result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=CARPETA_ORIGEN)
        if result.returncode == 0:
            print(f"[{datetime.now()}] No hay cambios para hacer commit.")
            return
        subprocess.run(["git", "commit", "-m", COMMIT_MENSAJE], cwd=CARPETA_ORIGEN, check=True)
        subprocess.run(["git", "push"], cwd=CARPETA_ORIGEN, check=True)
        print(f"[{datetime.now()}] Copia a GitHub realizada con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] Error durante backup a GitHub: {e}")

# FUNCIÓN: Copia incremental a NAS
def backup_nas(origen, destino):
    print(f"[{datetime.now()}] Iniciando copia incremental al NAS: {destino}")

    for carpeta_raiz, subdirs, archivos in os.walk(origen):
        rel_path = os.path.relpath(carpeta_raiz, origen)
        carpeta_destino = os.path.join(destino, rel_path)
        os.makedirs(carpeta_destino, exist_ok=True)

        for archivo in archivos:
            ruta_origen = os.path.join(carpeta_raiz, archivo)
            ruta_destino = os.path.join(carpeta_destino, archivo)

            if not os.path.exists(ruta_destino) or not filecmp.cmp(ruta_origen, ruta_destino, shallow=False):
                shutil.copy2(ruta_origen, ruta_destino)
                print(f"[{datetime.now()}] Copiado: {ruta_origen} → {ruta_destino}")
            else:
                print(f"[{datetime.now()}] Sin cambios: {ruta_origen}")

    print(f"[{datetime.now()}] Copia al NAS finalizada.")

# EJECUCIÓN
if __name__ == "__main__":
    backup_github()
    backup_nas(CARPETA_ORIGEN, CARPETA_DESTINO_NAS)

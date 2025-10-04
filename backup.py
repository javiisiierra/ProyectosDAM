import os
import subprocess
from pathlib import Path
from datetime import datetime

# 👇 Cambia esta ruta si tu carpeta no está en el escritorio
CARPETA_PROYECTOS = Path(r"C:\Users\usuario\Desktop\ProyectosDAM")

def log(mensaje):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{hora}] {mensaje}")

def backup_github():
    log("Iniciando copia de seguridad a GitHub...")
    for proyecto in CARPETA_PROYECTOS.iterdir():
        if proyecto.is_dir() and (proyecto / ".git").exists():
            log(f"Procesando: {proyecto.name}")
            try:
                subprocess.run(["git", "-C", str(proyecto), "add", "."], check=True)
                subprocess.run([
                    "git", "-C", str(proyecto), "commit",
                    "-m", f"Backup automático {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                ], check=True)
                subprocess.run(["git", "-C", str(proyecto), "push"], check=True)
                log(f"{proyecto.name} subido a GitHub con éxito.")
            except subprocess.CalledProcessError:
                log(f"No hay cambios o hubo un error en {proyecto.name}")
        else:
            log(f"{proyecto.name} no es un repositorio Git. Ignorado.")
    log("Copia de seguridad a GitHub finalizada.")

if __name__ == "__main__":
    backup_github()

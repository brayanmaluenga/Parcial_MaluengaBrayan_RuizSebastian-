"""Empaqueta la entrega del parcial en un ZIP verificado.

Uso: python scripts/empaquetar.py [ruta_del_video]

Genera dist/Parcial_MaluengaBrayan_RuizSebastian.zip con informe y anexo,
código, datos, pruebas y su última ejecución, README, evidencias y el video
(si existe). Excluye .git, __pycache__ y temporales. Verifica descomprimiendo
en /tmp, corriendo las pruebas desde ahí y listando el contenido.
"""

import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOMBRE = "Parcial_MaluengaBrayan_RuizSebastian"
EXCLUIR = {".git", "__pycache__", ".pytest_cache", "dist", ".venv", "venv"}

INCLUIR = [
    "README.md",
    "src",
    "data",
    "tests",
    "docs",
    "scripts",
    "evidencias",
]


def copiar(staging: Path) -> None:
    destino = staging / NOMBRE
    destino.mkdir(parents=True)

    for elemento in INCLUIR:
        origen = RAIZ / elemento
        if origen.is_dir():
            for ruta in origen.rglob("*"):
                if any(parte in EXCLUIR or parte in {"*.pyc"} for parte in ruta.parts):
                    continue
                if ruta.is_dir() and ruta.name in EXCLUIR:
                    continue
                if ruta.suffix == ".pyc" or ruta.name.endswith(".pyc"):
                    continue
                relativa = ruta.relative_to(RAIZ)
                if ruta.is_dir():
                    (destino / relativa).mkdir(parents=True, exist_ok=True)
                else:
                    destino.joinpath(relativa).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ruta, destino / relativa)
        else:
            shutil.copy2(origen, destino / elemento)

    video = RAIZ / "evidencias" / "demostracion.mp4"
    if video.exists():
        print(f"[1/5] Video incluido: {video.name}")
    else:
        print(
            "[1/5] AVISO: no existe evidencias/demostracion.mp4; "
            "hay que agregarlo o enlazarlo desde README.md antes de entregar."
        )


def main() -> None:
    staging = Path(tempfile.mkdtemp(prefix="empaquetado_"))
    verificacion = Path(tempfile.mkdtemp(prefix="verificacion_"))
    try:
        print("[1/5] Copiando contenido")
        copiar(staging)

        zip_ruta = RAIZ / "dist" / f"{NOMBRE}.zip"
        zip_ruta.parent.mkdir(exist_ok=True)
        zip_ruta.unlink(missing_ok=True)

        print("[2/5] Creando el ZIP")
        with zipfile.ZipFile(zip_ruta, "w", zipfile.ZIP_DEFLATED) as archivo:
            for ruta in sorted((staging / NOMBRE).rglob("*")):
                if ruta.is_file():
                    archivo.write(ruta, ruta.relative_to(staging))

        print("[3/5] Descomprimiendo en /tmp para verificar")
        with zipfile.ZipFile(zip_ruta) as archivo:
            archivo.extractall(verificacion)

        print("[4/5] Probando la suite desde la copia descomprimida")
        resultado = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=verificacion / NOMBRE,
            capture_output=True,
            text=True,
        )
        resumen = (resultado.stdout + resultado.stderr).strip().splitlines()[-3:]
        for linea in resumen:
            print(f"    {linea}")
        if resultado.returncode != 0:
            raise SystemExit("FALLO: las pruebas no pasan dentro del ZIP")
        if "OK" not in resumen[-1]:
            raise SystemExit("FALLO: la suite no termina en OK dentro del ZIP")

        print("[5/5] Contenido del ZIP")
        with zipfile.ZipFile(zip_ruta) as archivo:
            for nombre in sorted(archivo.namelist()):
                print(f"    {nombre}")
            total = len(archivo.namelist())

        tamano = zip_ruta.stat().st_size / 1024
        print(f"OK: dist/{NOMBRE}.zip ({total} rutas, {tamano:.0f} KiB)")
    finally:
        shutil.rmtree(staging, ignore_errors=True)
        shutil.rmtree(verificacion, ignore_errors=True)


if __name__ == "__main__":
    main()

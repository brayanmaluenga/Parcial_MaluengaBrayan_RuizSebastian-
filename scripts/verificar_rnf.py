"""Verificación de los 3 RNF del parcial "La última transmisión".

Ejecuta procedimientos reproducibles y escribe el resultado real en
evidencias/verificacion_rnf.txt. Se ejecuta desde la raíz del repo:

    python scripts/verificar_rnf.py
"""

import io
import json
import subprocess
import sys
import tempfile
import time
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from main import cargar_historia, validar_historia, jugar


def ejecutar(historia, entradas):
    """Ejecuta una partida con entradas simuladas y devuelve la salida."""
    salida = io.StringIO()

    with patch("builtins.input", side_effect=entradas):
        with redirect_stdout(salida):
            jugar(historia)

    return salida.getvalue()


def verificar_rnf1():
    """RNF-1 Modificabilidad: contenido nuevo sin tocar src/."""
    resultados = []

    # a) La segunda historia carga, valida y corre con el mismo motor.
    segunda = cargar_historia(RAIZ / "data" / "segunda_historia.json")
    ok_validacion = validar_historia(segunda) == []
    try:
        salida = ejecutar(segunda, ["1", "1", "1", "s"])
        ok_partida = "[E4]" in salida
    except Exception as error:
        ok_partida = False
        salida = repr(error)
    resultados.append(
        f"  a) Segunda historia con el mismo motor: "
        f"validacion={'OK' if ok_validacion else 'FALLO'}, "
        f"partida={salida if not ok_partida else 'llega a su final [E4] OK'}"
    )

    # b) El commit historico ba32f1a combino contenido y motor (11+5
    #    lineas en src/), por lo que la modificabilidad se verifica con
    #    un experimento vivo: agregar una historia nueva a una copia
    #    del repo y comprobar que src/ queda byte a byte identico.
    resultados.append(
        "  b) Nota: el commit ba32f1a combino la segunda historia con cambios "
        "en src/ (11+5 lineas), por eso se usa un experimento vivo."
    )

    import shutil

    with tempfile.TemporaryDirectory() as temporal:
        copia = Path(temporal) / "repo"
        shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns(".git"))
        experimento = {
            "titulo": "Historia temporal RNF-1",
            "inicio": "Q1",
            "variables": {"estrella_vista": False},
            "escenas": [
                {
                    "id": "Q1",
                    "texto": "El cielo se despeja.",
                    "final": False,
                    "opciones": [
                        {
                            "id": "mirar",
                            "texto": "Mirar el cielo",
                            "destino": "Q2",
                            "condiciones": {},
                            "efectos": {"estrella_vista": True},
                        }
                    ],
                },
                {
                    "id": "Q2",
                    "texto": "Puedes desear.",
                    "final": False,
                    "opciones": [
                        {
                            "id": "desear",
                            "texto": "Desear",
                            "destino": "Q3",
                            "condiciones": {"estrella_vista": True},
                            "efectos": {},
                        },
                        {
                            "id": "seguir",
                            "texto": "Seguir de largo",
                            "destino": "Q3",
                            "condiciones": {},
                            "efectos": {},
                        },
                    ],
                },
                {"id": "Q3", "texto": "Fin temporal.", "final": True, "opciones": []},
            ],
        }
        (copia / "data" / "historia_temporal.json").write_text(
            json.dumps(experimento, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        ejecucion = subprocess.run(
            [sys.executable, str(copia / "src" / "main.py"),
             str(copia / "data" / "historia_temporal.json")],
            input="1\n1\ns\n",
            capture_output=True,
            text=True,
        )
        ok_partida_new = "[Q3]" in ejecucion.stdout

        iguales = all(
            (copia / relativa).read_bytes() == (RAIZ / relativa).read_bytes()
            for relativa in ["src/main.py"]
        )
        resultados.append(
            f"  c) Experimento: se agrego data/historia_temporal.json (escenas Q*, "
            f"condicion nueva) a una copia del repo; src/main.py identico byte a byte "
            f"({iguales}), la historia carga y corre hasta [Q3] ({ok_partida_new})."
        )

    cumple = ok_validacion and ok_partida and iguales and ok_partida_new
    metrica = "lineas de codigo src/ modificadas para agregar una historia = 0"
    return cumple, metrica, resultados


def verificar_rnf2():
    """RNF-2 Claridad de errores: 9/9 categorias con causa + campo/ID."""
    base = cargar_historia(RAIZ / "data" / "historia.json")
    categorias = []

    casos = [
        ("1_estructura_incorrecta", [
            (lambda h: h.update({"escenas": "no lista"}), "La historia debe contener una lista de escenas."),
        ]),
        ("2_campos_obligatorios_ausentes", [
            (lambda h: h.update({"titulo": ""}), "El título es obligatorio."),
            (lambda h: h["escenas"][0].pop("final"), "debe indicar si es final."),
        ]),
        ("3_inicio_inexistente", [
            (lambda h: h.update({"inicio": "E99"}), "La escena inicial 'E99' no existe."),
        ]),
        ("4_ids_escena_duplicados", [
            (lambda h: h["escenas"].append(json.loads(json.dumps(h["escenas"][0]))),
             "identificadores de escena duplicados: E1."),
        ]),
        ("5_ids_opcion_duplicados", [
            (lambda h: h["escenas"][1]["opciones"][1].update({"id": "investigar"}),
             "identificadores de opción duplicados en 'E2': investigar."),
        ]),
        ("6_destino_inexistente", [
            (lambda h: h["escenas"][0]["opciones"][0].update({"destino": "E99"}),
             "El destino 'E99' de la opción 'revisar' no existe."),
        ]),
        ("7_variable_no_declarada", [
            (lambda h: h["escenas"][0]["opciones"][0].update({"efectos": {"fantasma": True}}),
             "no está declarada."),
        ]),
        ("8_valor_no_booleano", [
            (lambda h: h["variables"].update({"conoce_origen": "si"}),
             "debe tener un valor booleano."),
            (lambda h: h["escenas"][2]["opciones"][0]["condiciones"].update({"conoce_origen": "si"}),
             "debe ser booleano."),
        ]),
        ("9_cantidad_opciones_vs_final", [
            (lambda h: h["escenas"][3].update({"opciones": [
                {"id": "extra", "texto": "Extra", "destino": "E5",
                 "condiciones": {}, "efectos": {}}]}),
             "no debe tener opciones."),
            (lambda h: h["escenas"][0].update({"opciones": []}),
             "debe tener al menos una opción."),
        ]),
    ]

    detalles = []
    cumplidas = 0

    for nombre, mutaciones in casos:
        ok_variante = True
        for mutar, esperado in mutaciones:
            historia = json.loads(json.dumps(base))
            mutar(historia)
            errores = validar_historia(historia)
            if not any(esperado in error for error in errores):
                ok_variante = False
                detalles.append(f"  FALLO en {nombre}: no aparecio '{esperado}'")

        if ok_variante:
            cumplidas += 1
        detalles.append(
            f"  {nombre}: {'OK (mensaje con causa y campo/ID)' if ok_variante else 'FALLO'}"
        )

    # Archivo ilegible: excepcion controlada con causa, sin abrir sesion.
    with tempfile.TemporaryDirectory() as temporal:
        ruta = Path(temporal) / "ilegible.json"
        ruta.write_bytes(b"{ no es json ")
        try:
            cargar_historia(ruta)
            detalle_ilegible = "FALLO: no se rechazo el archivo ilegible"
        except json.JSONDecodeError as error:
            detalle_ilegible = f"OK (rechazo controlado): {type(error).__name__}"
    detalles.append(f"  archivo_ilegible: {detalle_ilegible}")

    metrica = f"{cumplidas}/9 categorias con mensaje de causa + campo/ID"
    return cumplidas == 9, metrica, detalles


def verificar_rnf3():
    """RNF-3 Confiabilidad: N entradas invalidas, 0 excepciones no controladas."""
    base = cargar_historia(RAIZ / "data" / "historia.json")
    resultados = []
    total = 0
    fallos = 0

    # a) Tormenta de 20 entradas invalidas en E2 y deshacer intacto.
    invalidas = [
        "0", "-1", "abc", "99", "r", "!", "#", "10", "2.5", "999999",
        " ", "1e2", "--", "0x1", "nul", "cinco", "tres", "4", "5", "6",
    ]
    entradas = ["1"] + invalidas + ["d", "1", "2", "2", "s"]
    total += len(invalidas)

    try:
        salida = ejecutar(base, entradas)
        estado_intacto = (
            salida.count("Opción inválida o no habilitada.") == 8
            and salida.count("Entrada inválida. Escribe un número o d.") == 12
            and salida.count("[E2]") == 22   # llegada + 20 invalidas + 1 visita posterior
            and "Decisión deshecha." in salida           # deshacer regresa a E1
            and salida.count("[E1]") == 2
            and "[E6]" in salida                         # la partida sigue funcionando
        )
        if not estado_intacto:
            fallos += 1
        resultados.append(
            f"  a) {len(invalidas)} entradas invalidas en E2: sin excepciones, "
            f"estado intacto ({'OK' if estado_intacto else 'FALLO'}), "
            f"despues deshacer regresa a E1 y la partida continua hasta [E6]."
        )
    except Exception as error:
        fallos += 1
        resultados.append(f"  a) EXCEPCION NO CONTROLADA: {error!r}")

    # b) Archivos JSON malformados: rechazo controlado.
    malformados = [b"{ no es json ", b'{"titulo": }', b"[\x00"]
    for contenido in malformados:
        total += 1
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "m.json"
            ruta.write_bytes(contenido)
            try:
                cargar_historia(ruta)
                fallos += 1
                resultados.append(f"  b) FALLO: {contenido!r} no fue rechazado")
            except json.JSONDecodeError:
                pass
    resultados.append(
        f"  b) {len(malformados)} archivos JSON malformados: rechazo controlado "
        f"(json.JSONDecodeError), sin abrir sesion."
    )

    # c) Historias con claves faltantes: rechazo controlado por el validador.
    faltantes = [
        {"titulo": "sin inicio", "variables": {}, "escenas": base["escenas"]},
        {"inicio": "E1", "variables": {}, "escenas": base["escenas"]},
    ]
    for historia in faltantes:
        total += 1
        try:
            errores = validar_historia(historia)
            if not errores:
                fallos += 1
                resultados.append("  c) FALLO: historia incompleta aceptada")
        except Exception as error:
            fallos += 1
            resultados.append(f"  c) EXCEPCION NO CONTROLADA: {error!r}")
    resultados.append(
        f"  c) {len(faltantes)} historias con claves faltantes: rechazadas por el "
        f"validador con diagnostico, sin exceptiones."
    )

    metrica = f"0 fallos en {total} entradas/casos invalidos"
    return fallos == 0, metrica, resultados


def verificar_rnf01_informe():
    """RNF-01 del informe: procesar una decision valida y mostrar la siguiente
    escena en <= 1 s en >= 95 % de ejecuciones, excluyendo la escritura del
    usuario. Se ejecuta N=1000 decisiones (mas estricto que las 100 del
    informe) aplicando la misma regla de aceptacion.
    """
    historia = {
        "titulo": "Historia de tiempo RNF-01",
        "inicio": "X1",
        "variables": {},
        "escenas": [
            {
                "id": "X1",
                "texto": "Unica escena con una opcion.",
                "final": False,
                "opciones": [
                    {
                        "id": "o1",
                        "texto": "Avanzar",
                        "destino": "X2",
                        "condiciones": {},
                        "efectos": {},
                    }
                ],
            },
            {"id": "X2", "texto": "Escena siguiente.", "final": True, "opciones": []},
        ],
    }

    n = 1000
    tiempos_ms = []
    for _ in range(n):
        inicio = time.perf_counter()
        ejecutar(historia, ["1", "s"])  # 1 decision valida + escena siguiente
        tiempos_ms.append((time.perf_counter() - inicio) * 1000.0)

    tiempos_ms.sort()
    media = sum(tiempos_ms) / n
    p95 = tiempos_ms[int(n * 0.95) - 1]
    maximo = tiempos_ms[-1]
    bajo_umbral = sum(1 for t in tiempos_ms if t <= 1000.0)
    fraccion = bajo_umbral / n

    detalles = [
        "  a) Definicion exacta del informe (seccion 3.2, sin cambiarla): "
        "'el sistema debera procesar una decision valida y mostrar la siguiente "
        "escena en un maximo de un segundo en al menos el 95 % de 100 ejecuciones "
        "automatizadas, excluyendo el tiempo de escritura del usuario.'",
        f"  b) Datos: N={n} decisiones validas procesadas por jugar() con entrada "
        "simulada (excluye la escritura del usuario, como pide la definicion).",
        f"  c) Tiempo medio = {media:.3f} ms | p95 = {p95:.3f} ms | maximo = {maximo:.3f} ms.",
        f"  d) Resultado contra el umbral del informe: {bajo_umbral}/{n} ejecuciones "
        f"({fraccion * 100:.1f} %) quedaron en <= 1000 ms (requiere >= 95 %).",
    ]
    cumple = fraccion >= 0.95
    metrica = f"{fraccion * 100:.1f} % de ejecuciones <= 1 s (umbral del informe: >= 95 %)"
    return cumple, metrica, detalles


def main():
    lineas = [
        f"=== Ejecucion de verificacion — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===",
        f"Python: {sys.version.split()[0]} | SO: {sys.platform}",
        "Script: scripts/verificar_rnf.py",
        "Nota de etiquetas: 'RNF-1/RNF-2/RNF-3' de este script son las "
        "verificaciones de modificabilidad/claridad/confiabilidad; el "
        "RNF-01 del INFORME (tiempo de respuesta) se verifica aparte.",
        "",
    ]

    for numero, nombre, verificar in [
        ("RNF-1", "Modificabilidad", verificar_rnf1),
        ("RNF-2", "Claridad de errores", verificar_rnf2),
        ("RNF-3", "Confiabilidad", verificar_rnf3),
        ("RNF-01 del informe", "Tiempo de respuesta", verificar_rnf01_informe),
    ]:
        try:
            cumple, metrica, detalles = verificar()
        except Exception as error:
            cumple, metrica, detalles = False, "ERROR EN EL PROCEDIMIENTO", [f"  {error!r}"]
        lineas.append(f"{numero} {nombre}")
        lineas.append(f"  Resultado: {'CUMPLE' if cumple else 'NO CUMPLE'}")
        lineas.append(f"  Metrica: {metrica}")
        lineas.extend(detalles)
        lineas.append("")

    destino = RAIZ / "evidencias" / "verificacion_rnf.txt"
    previa = destino.read_text(encoding="utf-8") if destino.exists() else ""
    destino.write_text(
        (previa.rstrip("\n") + "\n\n" if previa else "") + "\n".join(lineas) + "\n",
        encoding="utf-8",
    )  # agrega a lo existente, sin borrar ejecuciones previas
    print("\n".join(lineas))


if __name__ == "__main__":
    main()

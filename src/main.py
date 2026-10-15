
import json
from pathlib import Path


def cargar_historia(ruta):
    """Carga la historia desde un archivo JSON."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def buscar_escena(historia, id_escena):
    """Busca una escena por su identificador."""
    for escena in historia["escenas"]:
        if escena["id"] == id_escena:
            return escena

    raise ValueError(f"La escena '{id_escena}' no existe.")


def comprobar_condiciones(condiciones, variables):
    """Comprueba si se cumplen todas las condiciones."""
    for nombre, valor_esperado in condiciones.items():
        if nombre not in variables:
            return False

        if variables[nombre] != valor_esperado:
            return False

    return True



def escena_bloqueada(escena, variables):
    """Indica si una escena no final no tiene ninguna opción habilitada."""
    if escena["final"]:
        return False

    return not any(
        comprobar_condiciones(opcion["condiciones"], variables)
        for opcion in escena["opciones"]
    )


def jugar(historia):
    print(f"\n=== {historia['titulo']} ===")

    while True:
        # Reiniciar el estado de una nueva partida.
        escena_actual = historia["inicio"]
        variables = historia["variables"].copy()
        historial_deshacer = None

        while True:
            escena = buscar_escena(historia, escena_actual)

            print("\n" + "=" * 50)
            print(f"[{escena['id']}]")
            print(escena["texto"])

            # En un final, todavía se puede deshacer la última elección.
            if escena["final"]:
                print("\n[r] Reiniciar partida")
                print("[s] Salir")

                if historial_deshacer is not None:
                    print("[d] Deshacer última decisión")

                respuesta = input("Selecciona una acción: ").strip().lower()

                if respuesta == "d":
                    if historial_deshacer is None:
                        print("No hay ninguna decisión para deshacer.")
                        continue

                    escena_actual = historial_deshacer["escena"]
                    variables = historial_deshacer["variables"].copy()

                    # El retroceso se consume.
                    historial_deshacer = None

                    print("Decisión deshecha.")
                    continue

                if respuesta == "r":
                    # El bucle exterior inicia una partida limpia.
                    print("Reiniciando partida...")
                    break

                if respuesta == "s":
                    print("Gracias por jugar. Fin de la transmisión.")
                    return

                print("Acción inválida. Intenta nuevamente.")
                continue

            opciones_disponibles = []

            for opcion in escena["opciones"]:
                condiciones = opcion["condiciones"]

                if comprobar_condiciones(condiciones, variables):
                    opciones_disponibles.append(opcion)

            # Escena no final sin opciones habilitadas: partida bloqueada.
            if escena_bloqueada(escena, variables):
                print(
                    "\nPartida bloqueada: ninguna opción está habilitada "
                    f"en la escena '{escena['id']}'."
                )
                print("[d] Deshacer última decisión")
                print("[r] Reiniciar partida")
                print("[s] Salir")

                respuesta = input("Selecciona una acción: ").strip().lower()

                if respuesta == "d":
                    if historial_deshacer is None:
                        print("No hay ninguna decisión para deshacer.")
                        continue

                    escena_actual = historial_deshacer["escena"]
                    variables = historial_deshacer["variables"].copy()

                    historial_deshacer = None

                    print("Decisión deshecha.")
                    continue

                if respuesta == "r":
                    print("Reiniciando partida...")
                    break

                if respuesta == "s":
                    print("Gracias por jugar. Fin de la transmisión.")
                    return

                print("Acción inválida. Intenta nuevamente.")
                continue

            for numero, opcion in enumerate(
                opciones_disponibles, start=1
            ):
                print(f"{numero}. {opcion['texto']}")

            print("[d] Deshacer última decisión")

            respuesta = input("\nSelecciona una opción: ").strip().lower()

            if respuesta == "d":
                if historial_deshacer is None:
                    print("No hay ninguna decisión para deshacer.")
                    continue

                escena_actual = historial_deshacer["escena"]
                variables = historial_deshacer["variables"].copy()

                # Solo se permite un retroceso por elección válida.
                historial_deshacer = None

                print("Decisión deshecha.")
                continue

            # Validar que la entrada sea un número.
            try:
                seleccion = int(respuesta)
            except ValueError:
                print("Entrada inválida. Escribe un número o d.")
                continue

            if not 1 <= seleccion <= len(opciones_disponibles):
                print("Opción inválida o no habilitada.")
                continue

            opcion_elegida = opciones_disponibles[seleccion - 1]

            # Guardar el estado ANTERIOR a la elección válida.
            historial_deshacer = {
                "escena": escena_actual,
                "variables": variables.copy()
            }

            # Aplicar los efectos de la elección.
            for nombre, valor in opcion_elegida["efectos"].items():
                variables[nombre] = valor

            # Avanzar a la escena de destino.
            escena_actual = opcion_elegida["destino"]



def validar_historia(historia):
    """Comprueba errores estructurales en una historia."""
    errores = []

    # Comprobar los datos principales.
    if not isinstance(historia.get("titulo"), str) or not historia["titulo"].strip():
        errores.append("El título es obligatorio.")

    variables = historia.get("variables")
    if not isinstance(variables, dict):
        errores.append("Las variables deben ser un diccionario.")
        variables = {}

    for nombre, valor in variables.items():
        if not isinstance(valor, bool):
            errores.append(
                f"La variable '{nombre}' debe tener un valor booleano."
            )

    escenas = historia.get("escenas")
    if not isinstance(escenas, list) or not escenas:
        errores.append("La historia debe contener una lista de escenas.")
        return errores

    # Comprobar identificadores de escenas.
    ids_escenas = []
    for escena in escenas:
        if not isinstance(escena, dict) or not isinstance(escena.get("id"), str):
            errores.append("Hay una escena sin identificador válido.")
            continue

        ids_escenas.append(escena["id"])

    duplicados_escenas = sorted(
        identificador
        for identificador in set(ids_escenas)
        if ids_escenas.count(identificador) > 1
    )

    if duplicados_escenas:
        errores.append(
            "Hay identificadores de escena duplicados: "
            + ", ".join(duplicados_escenas)
            + "."
        )

    escenas_validas = {
        escena["id"]: escena
        for escena in escenas
        if isinstance(escena, dict)
        and isinstance(escena.get("id"), str)
    }

    inicio = historia.get("inicio")
    if inicio not in escenas_validas:
        if inicio is None:
            errores.append("La historia no indica la escena inicial.")
        else:
            errores.append(f"La escena inicial '{inicio}' no existe.")

    # Comprobar cada escena y sus opciones.
    for escena in escenas_validas.values():
        if not isinstance(escena.get("texto"), str):
            errores.append(f"La escena '{escena['id']}' no tiene texto válido.")

        if not isinstance(escena.get("final"), bool):
            errores.append(f"La escena '{escena['id']}' debe indicar si es final.")
            continue

        opciones = escena.get("opciones")
        if not isinstance(opciones, list):
            errores.append(f"Las opciones de '{escena['id']}' deben ser una lista.")
            continue

        if escena["final"] and opciones:
            errores.append(f"La escena final '{escena['id']}' no debe tener opciones.")

        if not escena["final"] and not opciones:
            errores.append(
                f"La escena no final '{escena['id']}' debe tener "
                "al menos una opción."
            )

        ids_opciones = []

        for opcion in opciones:
            if not isinstance(opcion, dict):
                errores.append(f"Hay una opción inválida en '{escena['id']}'.")
                continue

            id_opcion = opcion.get("id")
            if not isinstance(id_opcion, str) or not id_opcion:
                errores.append(f"Hay una opción sin identificador en '{escena['id']}'.")
            else:
                ids_opciones.append(id_opcion)

            if not isinstance(opcion.get("texto"), str):
                errores.append(f"Hay una opción sin texto válido en '{escena['id']}'.")

            if opcion.get("destino") not in escenas_validas:
                errores.append(
                    f"El destino '{opcion.get('destino')}' de la opción "
                    f"'{id_opcion}' no existe."
                )

            for campo in ("condiciones", "efectos"):
                datos = opcion.get(campo)

                if not isinstance(datos, dict):
                    errores.append(
                        f"El campo '{campo}' de '{id_opcion}' debe ser un diccionario."
                    )
                    continue

                for nombre, valor in datos.items():
                    if nombre not in variables:
                        errores.append(
                            f"La variable '{nombre}' de '{id_opcion}' no está declarada."
                        )
                    elif not isinstance(valor, bool):
                        errores.append(
                            f"El valor de '{nombre}' en '{id_opcion}' debe ser booleano."
                        )

        duplicados_opciones = sorted(
            identificador
            for identificador in set(ids_opciones)
            if ids_opciones.count(identificador) > 1
        )

        if duplicados_opciones:
            errores.append(
                "Hay identificadores de opción duplicados en "
                f"'{escena['id']}': {', '.join(duplicados_opciones)}."
            )

    return errores


    
def main():
    import sys

    if len(sys.argv) > 1:
        ruta = Path(sys.argv[1]).resolve()
    else:
        ruta = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "historia.json"
        )

    try:
        historia = cargar_historia(ruta)
        errores = validar_historia(historia)

        if errores:
            print("La historia contiene errores:")
            for error in errores:
                print(f"- {error}")
            return

        print("Validación correcta. La historia está lista.")
        jugar(historia)

    except (OSError, json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Error al ejecutar la historia: {error}")


if __name__ == "__main__":
    main()

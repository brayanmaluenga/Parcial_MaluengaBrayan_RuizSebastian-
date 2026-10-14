
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


def jugar(historia):
    escena_actual = historia["inicio"]

    # Copiamos las variables iniciales para no modificar la historia original.
    variables = historia["variables"].copy()

    print(f"\n=== {historia['titulo']} ===")

    while True:
        escena = buscar_escena(historia, escena_actual)

        print("\n" + "=" * 50)
        print(f"[{escena['id']}]")
        print(escena["texto"])

        # Si la escena es final, termina la partida.
        if escena["final"]:
            print("\nFIN DE LA TRANSMISIÓN")
            break

        # Mostrar solamente las opciones cuyas condiciones se cumplen.
        opciones_disponibles = []

        for opcion in escena["opciones"]:
            condiciones = opcion["condiciones"]

            if comprobar_condiciones(condiciones, variables):
                opciones_disponibles.append(opcion)

        if not opciones_disponibles:
            print("Error: no hay opciones disponibles.")
            break

        for numero, opcion in enumerate(opciones_disponibles, start=1):
            print(f"{numero}. {opcion['texto']}")

        # Solicitar una opción válida.
        while True:
            respuesta = input("\nSelecciona una opción: ")

            try:
                seleccion = int(respuesta)

                if 1 <= seleccion <= len(opciones_disponibles):
                    break

                print("Selecciona un número de las opciones mostradas.")

            except ValueError:
                print("Entrada inválida. Debes escribir un número.")

        opcion_elegida = opciones_disponibles[seleccion - 1]

        # Aplicar los efectos de la decisión.
        for nombre, valor in opcion_elegida["efectos"].items():
            variables[nombre] = valor

        # Avanzar a la siguiente escena.
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

    if len(ids_escenas) != len(set(ids_escenas)):
        errores.append("Hay identificadores de escena duplicados.")

    escenas_validas = {
        escena["id"]: escena
        for escena in escenas
        if isinstance(escena, dict)
        and isinstance(escena.get("id"), str)
    }

    inicio = historia.get("inicio")
    if inicio not in escenas_validas:
        errores.append("La escena inicial no existe.")

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
                    f"El destino de la opción '{id_opcion}' no existe."
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

        if len(ids_opciones) != len(set(ids_opciones)):
            errores.append(
                f"Hay identificadores de opción duplicados en '{escena['id']}'."
            )

    return errores


def main():
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

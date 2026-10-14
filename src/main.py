
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


def main():
    ruta = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "historia.json"
    )

    try:
        historia = cargar_historia(ruta)
        jugar(historia)

    except (OSError, json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Error al ejecutar la historia: {error}")


if __name__ == "__main__":
    main()

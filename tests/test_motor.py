




import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

RUTA_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(RUTA_SRC))

from main import (
    cargar_historia,
    comprobar_condiciones,
    buscar_escena,
    validar_historia,
    jugar,
)


def ejecutar(historia, entradas):
    """Ejecuta una partida con entradas simuladas y devuelve la salida."""
    salida = StringIO()

    with patch("builtins.input", side_effect=entradas):
        with redirect_stdout(salida):
            jugar(historia)

    return salida.getvalue()


class TestMotorNarrativo(unittest.TestCase):

    def setUp(self):
        ruta = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "historia.json"
        )
        self.historia = cargar_historia(ruta)

    def test_historia_del_profesor_es_valida(self):
        """Validación previa: la historia real no produce errores."""
        errores = validar_historia(self.historia)
        self.assertEqual(errores, [])

    def test_detecta_destino_inexistente(self):
        """U4 (variante suelta): destino inexistente produce diagnóstico."""
        historia = json.loads(json.dumps(self.historia))
        historia["escenas"][0]["opciones"][0]["destino"] = "E99"

        errores = validar_historia(historia)

        self.assertTrue(
            any("destino" in error.lower() for error in errores)
        )

    def test_detecta_variable_no_declarada(self):
        """U4 (variante suelta): variable no declarada produce diagnóstico."""
        historia = json.loads(json.dumps(self.historia))
        historia["escenas"][0]["opciones"][0]["efectos"] = {
            "variable_inexistente": True
        }

        errores = validar_historia(historia)

        self.assertTrue(
            any("no está declarada" in error for error in errores)
        )

    def test_detecta_escenas_duplicadas(self):
        """U4 (variante suelta): IDs de escena duplicados son detectados."""
        historia = json.loads(json.dumps(self.historia))
        historia["escenas"].append(
            json.loads(json.dumps(historia["escenas"][0]))
        )

        errores = validar_historia(historia)

        self.assertTrue(
            any("duplicados" in error.lower() for error in errores)
        )

    def test_RF08_segunda_historia_sin_modificar_el_motor(self):
        """RF-08: la segunda historia carga y corre con el mismo motor.

        Verifica la separación contenido/motor: un archivo JSON nuevo
        con sus propias escenas, condiciones y efectos funciona sin
        tocar src/.
        """
        ruta = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "segunda_historia.json"
        )
        historia = cargar_historia(ruta)

        self.assertEqual(validar_historia(historia), [])

        resultado = ejecutar(historia, ["1", "1", "1", "s"])

        self.assertIn("La señal del refugio", resultado)
        self.assertIn("[E4]", resultado)

    def test_U1_condiciones_habilitan_solo_opciones_correspondientes(self):
        """U1: las condiciones habilitan únicamente las opciones correspondientes.

        En E3, con conoce_origen verdadero solo se habilitan
        'activar_codigo' y 'cortar'; con falso, 'activar_sin_verificar'
        y 'cortar' (exactamente dos opciones en cada caso).
        """
        escena = buscar_escena(self.historia, "E3")
        variantes = [
            (True, {"activar_codigo", "cortar"}),
            (False, {"activar_sin_verificar", "cortar"}),
        ]

        for conoce_origen, ids_esperados in variantes:
            with self.subTest(conoce_origen=conoce_origen):
                variables = dict(self.historia["variables"])
                variables["conoce_origen"] = conoce_origen

                habilitadas = [
                    opcion["id"]
                    for opcion in escena["opciones"]
                    if comprobar_condiciones(
                        opcion["condiciones"], variables
                    )
                ]

                self.assertEqual(len(habilitadas), 2)
                self.assertEqual(set(habilitadas), ids_esperados)

    def test_U2_eleccion_valida_aplica_efectos_y_avanza(self):
        """U2: una elección válida aplica los efectos y avanza al destino.

        Revisar señal lleva a E2; investigar archivo aplica
        conoce_origen=verdadero (se demuestra porque en E3 se habilita
        'Activar con código') y avanza a E3; activar con código lleva a E4.
        """
        resultado = ejecutar(self.historia, ["1", "1", "1", "s"])

        self.assertIn("[E2]", resultado)
        self.assertIn("[E3]", resultado)
        self.assertIn("[E4]", resultado)
        self.assertIn("Activar con código", resultado)

    def test_U3_entrada_invalida_deja_estado_intacto_y_preserva_historial(self):
        """U3: una opción inexistente o no habilitada deja el estado intacto.

        En E2 se intenta la opción 5 (inexistente): la escena se
        reimprime sin avanzar. Después, deshacer regresa a E1, lo que
        demuestra que el historial de la última elección válida no fue
        sustituido por la entrada inválida.
        """
        resultado = ejecutar(
            self.historia, ["1", "5", "d", "1", "2", "2", "s"]
        )

        self.assertIn("Opción inválida o no habilitada.", resultado)
        self.assertEqual(resultado.count("[E2]"), 3)
        self.assertEqual(resultado.count("[E1]"), 2)
        self.assertIn("[E6]", resultado)

    def test_U4_validacion_nueve_categorias(self):
        """U4: los errores de contenido obligatorios producen diagnóstico controlado.

        Prueba parametrizada con las nueve categorías de la guía.
        Cada variante verifica que el mensaje indique la causa y, cuando
        el mensaje lo incluye, el campo o ID involucrado. Las variantes
        de la categoría 9 (cantidad de opciones incompatible con final)
        están aquí con subTest; 'archivo_ilegible' se comprueba con
        assertRaises sobre cargar_historia.
        """
        variantes = [
            (
                "estructura_incorrecta",
                lambda h: h.update({"escenas": "no soy una lista"}),
                "La historia debe contener una lista de escenas.",
                None,
            ),
            (
                "campo_titulo_ausente",
                lambda h: h.update({"titulo": ""}),
                "El título es obligatorio.",
                "título",
            ),
            (
                "campo_final_ausente",
                lambda h: h["escenas"][0].pop("final"),
                "debe indicar si es final.",
                "E1",
            ),
            (
                "inicio_inexistente",
                lambda h: h.update({"inicio": "E99"}),
                "La escena inicial 'E99' no existe.",
                "E99",
            ),
            (
                "ids_escena_duplicados",
                lambda h: h["escenas"].append(
                    json.loads(json.dumps(h["escenas"][0]))
                ),
                "identificadores de escena duplicados: E1.",
                "E1",
            ),
            (
                "ids_opcion_duplicados",
                lambda h: h["escenas"][1]["opciones"][1].update(
                    {"id": "investigar"}
                ),
                "identificadores de opción duplicados en 'E2': investigar.",
                "investigar",
            ),
            (
                "destino_inexistente",
                lambda h: h["escenas"][0]["opciones"][0].update(
                    {"destino": "E99"}
                ),
                "El destino 'E99' de la opción 'revisar' no existe.",
                "E99",
            ),
            (
                "variable_no_declarada",
                lambda h: h["escenas"][0]["opciones"][0].update(
                    {"efectos": {"variable_fantasma": True}}
                ),
                "no está declarada.",
                "variable_fantasma",
            ),
            (
                "valor_no_booleano_variables",
                lambda h: h["variables"].update({"conoce_origen": "verdadero"}),
                "debe tener un valor booleano.",
                "conoce_origen",
            ),
            (
                "valor_no_booleano_condiciones",
                lambda h: h["escenas"][2]["opciones"][0]["condiciones"].update(
                    {"conoce_origen": "sí"}
                ),
                "debe ser booleano.",
                "activar_codigo",
            ),
            (
                "final_con_opciones",
                lambda h: h["escenas"][3].update(
                    {
                        "opciones": [
                            {
                                "id": "extra",
                                "texto": "Extra",
                                "destino": "E5",
                                "condiciones": {},
                                "efectos": {},
                            }
                        ]
                    }
                ),
                "no debe tener opciones.",
                "E4",
            ),
            (
                "no_final_sin_opciones",
                lambda h: h["escenas"][0].update({"opciones": []}),
                "debe tener al menos una opción.",
                "E1",
            ),
        ]

        for nombre, mutar, mensaje_esperado, id_esperado in variantes:
            with self.subTest(variante=nombre):
                historia = json.loads(json.dumps(self.historia))
                mutar(historia)

                errores = validar_historia(historia)

                self.assertTrue(
                    any(mensaje_esperado in error for error in errores),
                    f"No se detectó: {mensaje_esperado}",
                )

                if id_esperado is not None:
                    self.assertTrue(
                        any(id_esperado in error for error in errores),
                        f"El mensaje no identifica: {id_esperado}",
                    )

        # Variante especial: archivo ilegible (JSON malformado).
        with self.subTest(variante="archivo_ilegible"):
            with tempfile.TemporaryDirectory() as temporal:
                ruta = Path(temporal) / "ilegible.json"
                ruta.write_bytes(b"{ esto no es json ")

                with self.assertRaises(json.JSONDecodeError):
                    cargar_historia(ruta)

    def test_U6_variantes_de_deshacer(self):
        """U6 (variantes): reglas de deshacer según el anexo.

        - Al iniciar no hay retroceso disponible.
        - Desde E4 y desde E6 se regresa a E3 con los valores previos.
        (La variante de entrada inválida y la de nueva elección que
        re-habilita el retroceso, así como deshacer desde E5, quedan
        cubiertas en test_U6_deshacer_restaurar_estado... e I1.)
        """
        variantes = [
            (
                "sin_retroceso_al_inicio",
                ["d", "1", "1", "1", "s"],
                ["No hay ninguna decisión para deshacer.", "[E4]"],
            ),
            (
                "deshacer_desde_E4",
                ["1", "1", "1", "d", "2", "1", "s"],
                ["[E4]", "Decisión deshecha.", "[E3]", "[E6]"],
            ),
            (
                "deshacer_desde_E6",
                ["1", "2", "2", "d", "1", "s"],
                ["[E6]", "Decisión deshecha.", "[E3]", "[E5]"],
            ),
        ]

        for nombre, entradas, esperados in variantes:
            with self.subTest(variante=nombre):
                resultado = ejecutar(self.historia, entradas)

                for esperado in esperados:
                    self.assertIn(esperado, resultado)

    def test_CA01_mostrar_exactamente_dos_opciones_en_e3(self):
        """CA01: revisar + investigar deja la sesión en E3 con conoce_origen verdadero.

        En E3 deben verse exactamente dos opciones: 'Activar con código'
        y 'Cortar comunicación'.
        """
        resultado = ejecutar(self.historia, ["1", "1", "1", "s"])

        self.assertIn("[E3]", resultado)
        self.assertIn("1. Activar con código", resultado)
        self.assertIn("2. Cortar comunicación", resultado)
        self.assertNotIn("Activar sin verificar", resultado)

    def test_CA02_opcion_no_habilitada_rechazada_id_directo(self):
        """CA02: 'activar_codigo' no puede ejecutarse sin conocer el origen.

        El motor no muestra la opción y, si se envía su identificador
        directamente, la entrada es rechazada sin avanzar: solo acepta
        índices de la lista de opciones habilitadas.
        """
        resultado = ejecutar(
            self.historia, ["1", "2", "activar_codigo", "1", "s"]
        )

        self.assertNotIn("Activar con código", resultado)
        self.assertIn("Entrada inválida. Escribe un número o d.", resultado)
        self.assertIn("[E5]", resultado)

        escena = buscar_escena(self.historia, "E3")
        activar = next(
            opcion
            for opcion in escena["opciones"]
            if opcion["id"] == "activar_codigo"
        )
        self.assertFalse(
            comprobar_condiciones(
                activar["condiciones"], {"conoce_origen": False}
            )
        )

    def test_CA03_destino_e99_rechazado_sin_abrir_sesion(self):
        """CA03: un destino E99 inexistente se rechaza sin abrir sesión.

        La copia del contenido con destino E99 se carga con main(); la
        carga se rechaza y nunca se abre una sesión jugable.
        """
        historia = json.loads(json.dumps(self.historia))
        historia["escenas"][0]["opciones"][0]["destino"] = "E99"

        import main as modulo_main

        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "copia_e99.json"
            ruta.write_text(json.dumps(historia), encoding="utf-8")

            salida = StringIO()
            with patch.object(sys, "argv", ["main.py", str(ruta)]):
                with redirect_stdout(salida):
                    modulo_main.main()

        resultado = salida.getvalue()

        self.assertIn("La historia contiene errores", resultado)
        self.assertIn("no existe", resultado)
        self.assertNotIn("Validación correcta", resultado)
        self.assertNotIn("[E1]", resultado)

    def test_I1_recorre_los_tres_finales(self):
        """I1 (extendida): con el archivo real, carga y decisiones hasta los tres finales.

        E4 requiere investigar el archivo; E5 y E6 se alcanzan sin
        investigar. Deshacer desde un final está cubierto en
        test_I1_deshacer_desde_final_con_historia_cargada.
        """
        rutas = [
            ("E4", ["1", "1", "1", "s"]),
            ("E5", ["1", "2", "1", "s"]),
            ("E6", ["1", "2", "2", "s"]),
        ]

        for final, entradas in rutas:
            with self.subTest(final=final):
                resultado = ejecutar(self.historia, entradas)

                self.assertIn(f"[{final}]", resultado)
                self.assertIn("Fin de la transmisión.", resultado)


    def test_U6_deshacer_restaurar_estado_y_consumir_historial(self):
        """U6: deshacer restaura escena y variables y consume el retroceso.

        Cubre el ejemplo del anexo: desde E2, investigar lleva a E3 con
        conoce_origen verdadero; deshacer devuelve a E2 con
        conoce_origen falso; un segundo intento no cambia nada; al
        continuar sin investigar, E3 muestra 'Activar sin verificar' y
        'Cortar comunicación'. Incluye además las variantes de entrada
        inválida que preserva el historial y de nueva elección que
        vuelve a habilitar un retroceso.
        """
        salida = StringIO()

        # Investigar, intentar una opción inválida, deshacer,
        # intentar deshacer otra vez, continuar sin investigar,
        # elegir un final, deshacer desde ese final y salir.
        entradas = [
            "1", "1", "99", "d", "d",
            "2", "1", "d", "2", "s"
        ]

        with patch("builtins.input", side_effect=entradas):
            with redirect_stdout(salida):
                jugar(self.historia)

        resultado = salida.getvalue()

        # La entrada inválida no debe impedir el retroceso.
        self.assertIn("Opción inválida o no habilitada.", resultado)

        # El segundo retroceso debe rechazarse.
        self.assertIn("No hay ninguna decisión para deshacer.", resultado)

        # La nueva elección debe volver a habilitar el retroceso.
        self.assertGreaterEqual(
            resultado.count("Decisión deshecha."), 2
        )

        # Se puede deshacer desde un final y volver a E3.
        self.assertIn("[E5]", resultado)
        self.assertIn("[E3]", resultado)

        # Tras deshacer la investigación, se regresa a E2 (ejemplo del
        # anexo) y se debe poder continuar sin investigar y activar la
        # antena sin verificar.
        self.assertIn("[E2]", resultado)
        self.assertIn("Activar sin verificar", resultado)
        self.assertIn("Cortar", resultado)

    def test_U5_reiniciar_elimina_el_historial(self):
        """U5 (extendida): reiniciar restaura escena y variables iniciales y elimina el historial.

        Tras reiniciar, no hay decisión que deshacer; la partida vuelve
        a E1 y las variables quedan en sus valores iniciales: continuar
        sin investigar muestra 'Activar sin verificar' (si conoce_origen
        no se hubiera restaurado a falso, mostraría 'Activar con código').
        """
        salida = StringIO()

        # Investigar hasta un final, reiniciar, comprobar que no hay
        # historial, continuar sin investigar y terminar.
        entradas = [
            "1", "1", "1", "r",
            "d", "1", "2", "2", "s"
        ]

        with patch("builtins.input", side_effect=entradas):
            with redirect_stdout(salida):
                jugar(self.historia)

        resultado = salida.getvalue()

        self.assertIn("Reiniciando partida...", resultado)
        self.assertIn("No hay ninguna decisión para deshacer.", resultado)
        self.assertGreaterEqual(resultado.count("[E1]"), 2)
        self.assertIn("Activar sin verificar", resultado)

    
    def test_I1_deshacer_desde_final_con_historia_cargada(self):
        """I1 (extendida): carga real del archivo + deshacer desde un final.

        Con el archivo real cargado, continuar sin investigar llega a
        E5; desde E5, deshacer regresa a E3 y cortar lleva a E6.
        """
        salida = StringIO()

        # Continuar sin investigar permite llegar a E5.
        # Desde E5, deshacer debe regresar a E3.
        entradas = ["1", "2", "1", "d", "2", "s"]

        with patch("builtins.input", side_effect=entradas):
            with redirect_stdout(salida):
                jugar(self.historia)

        resultado = salida.getvalue()

        self.assertIn("[E5]", resultado)
        self.assertIn("Decisión deshecha.", resultado)
        self.assertIn("[E3]", resultado)
        self.assertIn("[E6]", resultado)


class TestBloqueo(unittest.TestCase):

    def setUp(self):
        ruta = (
            Path(__file__).resolve().parent
            / "historia_bloqueada.json"
        )
        self.historia = cargar_historia(ruta)

    def test_bloqueo_informa_y_permite_reiniciar(self):
        """Bloqueo (regla de la guía): informa y permite reiniciar sin bucle infinito."""
        salida = StringIO()

        # Ir directo deja P2 sin opciones habilitadas; desde el
        # bloqueo se reinicia, se vuelve a P1 y se sale por el final.
        entradas = ["2", "r", "1", "1", "s"]

        with patch("builtins.input", side_effect=entradas):
            with redirect_stdout(salida):
                jugar(self.historia)

        resultado = salida.getvalue()

        self.assertIn("Partida bloqueada", resultado)
        self.assertIn("'P2'", resultado)
        self.assertIn("Reiniciando partida...", resultado)
        self.assertIn("Fin de la transmisión.", resultado)

    def test_deshacer_libera_el_bloqueo(self):
        """Bloqueo + deshacer: retroceder puede re-habilitar la escena."""
        salida = StringIO()

        # Ir directo bloquea P2; deshacer devuelve a P1 y elegir
        # tomar la llave habilita de nuevo la escena.
        entradas = ["2", "d", "1", "1", "s"]

        with patch("builtins.input", side_effect=entradas):
            with redirect_stdout(salida):
                jugar(self.historia)

        resultado = salida.getvalue()

        self.assertIn("Partida bloqueada", resultado)
        self.assertIn("'P2'", resultado)
        self.assertIn("Decisión deshecha.", resultado)
        self.assertEqual(resultado.count("Decisión deshecha."), 1)
        self.assertIn("[P3]", resultado)


if __name__ == "__main__":
    unittest.main()

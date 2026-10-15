




import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

RUTA_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(RUTA_SRC))

from main import cargar_historia, validar_historia, jugar


class TestMotorNarrativo(unittest.TestCase):

    def setUp(self):
        ruta = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "historia.json"
        )
        self.historia = cargar_historia(ruta)

    def test_historia_del_profesor_es_valida(self):
        errores = validar_historia(self.historia)
        self.assertEqual(errores, [])

    def test_detecta_destino_inexistente(self):
        historia = json.loads(json.dumps(self.historia))
        historia["escenas"][0]["opciones"][0]["destino"] = "E99"

        errores = validar_historia(historia)

        self.assertTrue(
            any("destino" in error.lower() for error in errores)
        )

    def test_detecta_variable_no_declarada(self):
        historia = json.loads(json.dumps(self.historia))
        historia["escenas"][0]["opciones"][0]["efectos"] = {
            "variable_inexistente": True
        }

        errores = validar_historia(historia)

        self.assertTrue(
            any("no está declarada" in error for error in errores)
        )

    def test_detecta_escenas_duplicadas(self):
        historia = json.loads(json.dumps(self.historia))
        historia["escenas"].append(
            json.loads(json.dumps(historia["escenas"][0]))
        )

        errores = validar_historia(historia)

        self.assertTrue(
            any("duplicados" in error.lower() for error in errores)
        )


    def test_U6_deshacer_restaurar_estado_y_consumir_historial(self):
        # Cargar la historia real del profesor.
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

        # Tras deshacer la investigación, se debe poder continuar
        # sin investigar y activar la antena sin verificar.
        self.assertIn("Activar sin verificar", resultado)

    def test_U5_reiniciar_elimina_el_historial(self):
        salida = StringIO()

        # Llegar a un final, reiniciar y comprobar que en E1
        # ya no existe una decisión que pueda deshacerse.
        entradas = [
            "1", "1", "1", "r",
            "d", "1", "d", "1", "2", "2", "s"
        ]

        with patch("builtins.input", side_effect=entradas):
            with redirect_stdout(salida):
                jugar(self.historia)

        resultado = salida.getvalue()

        self.assertIn("Reiniciando partida...", resultado)
        self.assertIn("No hay ninguna decisión para deshacer.", resultado)

    
    def test_I1_deshacer_desde_final_con_historia_cargada(self):
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


    def test_U4_cantidad_de_opciones_incompatible_con_final(self):
        historia_base = {
            "titulo": "Prueba",
            "inicio": "S1",
            "variables": {},
            "escenas": [
                {
                    "id": "S1",
                    "texto": "Escena de entrada.",
                    "final": False,
                    "opciones": [
                        {
                            "id": "o1",
                            "texto": "Opción única",
                            "destino": "S2",
                            "condiciones": {},
                            "efectos": {},
                        }
                    ],
                },
                {"id": "S2", "texto": "Final.", "final": True, "opciones": []},
            ],
        }

        variantes = [
            ("no_final_sin_opciones", "debe tener al menos una opción."),
            ("final_con_opciones", "no debe tener opciones."),
        ]

        for nombre, mensaje_esperado in variantes:
            with self.subTest(variante=nombre):
                historia = json.loads(json.dumps(historia_base))

                if nombre == "no_final_sin_opciones":
                    historia["escenas"][0]["opciones"] = []
                else:
                    historia["escenas"][1]["opciones"] = [
                        {
                            "id": "extra",
                            "texto": "Opción en final",
                            "destino": "S1",
                            "condiciones": {},
                            "efectos": {},
                        }
                    ]

                errores = validar_historia(historia)

                self.assertTrue(
                    any(mensaje_esperado in error for error in errores),
                    f"No se detectó: {mensaje_esperado}"
                )
                self.assertTrue(
                    any(
                        "S1" in error or "S2" in error
                        for error in errores
                    ),
                    "El mensaje no identifica la escena."
                )


if __name__ == "__main__":
    unittest.main()

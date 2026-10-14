




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


if __name__ == "__main__":
    unittest.main()

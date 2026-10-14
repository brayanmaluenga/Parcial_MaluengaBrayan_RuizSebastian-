
import json
import sys
import unittest
from pathlib import Path

# Permite importar el código ubicado en src.
sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "src")
)

from main import cargar_historia, validar_historia


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


if __name__ == "__main__":
    unittest.main()

# RF-06 — Deshacer la última decisión

**Identificador:** RF-06

**Nombre:** Deshacer la última decisión válida.

**Descripción:** El sistema permitirá al jugador deshacer su última decisión válida y regresar al estado inmediatamente anterior a dicha elección, restaurando la escena actual y todas las variables.

**Criterios de aceptación**

- CA-01: Al iniciar una partida, no habrá ninguna decisión disponible para deshacer.
- CA-02: Después de una elección válida, se podrá deshacer esa decisión una sola vez.
- CA-03: Al deshacer, se restaurarán exactamente la escena y las variables anteriores a la elección.
- CA-04: Un segundo intento de deshacer, sin una nueva elección válida, no modificará el estado del juego.
- CA-05: Las entradas inválidas o las opciones no habilitadas no modificarán el estado ni reemplazarán el historial de la última elección válida.
- CA-06: Deshacer estará disponible desde los finales E4, E5 y E6 cuando exista una elección válida que pueda revertirse.
- CA-07: Reiniciar la partida restaurará la escena inicial y las variables originales, y eliminará el historial de deshacer.

**Prioridad:** Alta.

**Trazabilidad:** Cambio solicitado por el cliente durante el parcial, correspondiente al requisito de deshacer y a las pruebas U6, U5 e I1.
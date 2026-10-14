\# Matriz de trazabilidad



\*\*Proyecto:\*\* La última transmisión  

\*\*Cambio:\*\* RF-06 — Deshacer la última decisión



| Requisito o actividad | Implementación | Prueba asociada |

|---|---|---|

| RF-06: Deshacer la última decisión válida | `jugar()` en `src/main.py` | `test\_U6\_deshacer\_restaurar\_estado\_y\_consumir\_historial` |

| Restaurar la escena y las variables anteriores | Restauración del estado guardado antes de la elección válida | `test\_U6\_deshacer\_restaurar\_estado\_y\_consumir\_historial` |

| Impedir un segundo deshacer sin una nueva elección válida | El historial se elimina después de deshacer | `test\_U6\_deshacer\_restaurar\_estado\_y\_consumir\_historial` |

| Mantener el historial ante entradas inválidas | Validación de la entrada antes de modificar el estado guardado | Verificar con una prueba de regresión de entrada inválida |

| Reiniciar sin conservar el historial | Reinicio de la partida en `jugar()` | `test\_U5\_reiniciar\_elimina\_el\_historial` |

| Deshacer desde una escena final | Opción de deshacer disponible en los finales cuando existe historial | `test\_I1\_deshacer\_desde\_final\_con\_historia\_cargada` |



\## Evidencia de verificación



La suite de pruebas ejecutada reportó \*\*7 pruebas correctas\*\* (`OK`). Esta evidencia corresponde a la ejecución realizada; cualquier prueba adicional deberá ejecutarse y registrarse por separado.



\## Relación con el cambio solicitado



El requisito RF-06 documenta el comportamiento esperado. La implementación se encuentra en `src/main.py` y las pruebas automatizadas, en `tests/test\_motor.py`.


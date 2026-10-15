# Matriz de trazabilidad

**Proyecto:** La última transmisión
**Cambio incorporado:** RF-06 — Deshacer la última decisión (solicitud del anexo de la hora 6)

Los requisitos funcionales RF-01 a RF-08 y los RNF-01 a RNF-03 provienen del
informe del equipo (`evidencias/Informe_parcial .pdf`, secciones 3.1 y 3.2).
La columna "Necesidad" hace el mapeo explícito con N01–N06 de la guía y con el
cambio solicitado. Los modelos citados son los de
`evidencias/Modelado_diagramas.pdf`.

## Requisitos funcionales

| ID | Necesidad | Modelo | Componente o archivo (ruta y función) | Prueba (archivo, nombre) | Evidencia (ruta de resultados) |
|---|---|---|---|---|---|
| RF-01 Carga de historias desde JSON | N01 | Diagrama de contexto; casos de uso (cargar y validar) | `src/main.py` — `cargar_historia()`; `main()` valida antes de abrir sesión | `tests/test_motor.py::test_historia_del_profesor_es_valida`; `test_U4_...` (archivo ilegible); `test_CA03_...` (rechazo sin abrir sesión) | `evidencias/resultados_pruebas_linux.txt`; `evidencias/verificacion_rnf.txt` |
| RF-02 Validación de historias | N06 | Casos de uso (cargar y validar) | `src/main.py` — `validar_historia()` (las 9 categorías con causa y campo/ID) | `test_U4_validacion_nueve_categorias` (subTest, 12 variantes); `test_detecta_destino_inexistente`; `test_detecta_variable_no_declarada`; `test_detecta_escenas_duplicadas` | `resultados_pruebas_linux.txt`; `verificacion_rnf.txt` (RNF-2: 9/9) |
| RF-03 Visualización de escena y solo opciones compatibles | N02 | Diagrama de contexto; secuencia "elegir una opción" | `src/main.py` — filtrado con `comprobar_condiciones()` en `jugar()`; bloqueo con `escena_bloqueada()` | `test_U1_condiciones_habilitan_...`; `test_CA01_...`; `test_CA02_...`; `TestBloqueo` (2 pruebas) | `resultados_pruebas_linux.txt` |
| RF-04 Procesamiento de decisiones (efectos y destino) | N03 | Secuencia "elegir una opción" | `src/main.py` — aplicación de `efectos` y avance en `jugar()`; rechazo de entradas inválidas | `test_U2_eleccion_valida_...`; `test_U3_entrada_invalida_...` | `resultados_pruebas_linux.txt` |
| RF-05 Gestión del estado y los finales | N04, N05 | Estados de una sesión; secuencia | `src/main.py` — `variables` e `historial_deshacer` en `jugar()`; escenas finales | `test_I1_recorre_los_tres_finales`; `test_U6_deshacer_...` | `resultados_pruebas_linux.txt` |
| RF-06 Deshacer la última decisión válida | Cambio del anexo (reemplaza el acuerdo provisional) | Estados de una sesión; secuencia | `src/main.py` — snapshot/restore de escena y variables en `jugar()`; especificado en `docs/RF-06-deshacer.md` (CA-01..CA-07) | `test_U6_deshacer_...`; `test_U6_variantes_de_deshacer`; `test_I1_deshacer_desde_final_...`; `test_U5_...` (sin historial tras reinicio); `test_deshacer_libera_el_bloqueo` | `resultados_pruebas_linux.txt` |
| RF-07 Reinicio de partida | N05 | Estados de una sesión (transición de reinicio) | `src/main.py` — bucle externo de `jugar()` restaura escena inicial y variables, y elimina el historial | `test_U5_reiniciar_elimina_el_historial`; `test_bloqueo_informa_y_permite_reiniciar` | `resultados_pruebas_linux.txt` |
| RF-08 Compatibilidad entre historias (motor genérico) | N01 | Componentes (contenido / motor / interfaz) | `src/main.py` — sin IDs de ninguna historia en el código; contenido en `data/` | `test_RF08_segunda_historia_sin_modificar_el_motor` | `resultados_pruebas_linux.txt`; `verificacion_rnf.txt` (RNF-1: 0 líneas en src/) |

## Requisitos no funcionales

| ID | Relación | Modelo | Componente o archivo | Prueba | Evidencia |
|---|---|---|---|---|---|
| RNF-01 Tiempo de respuesta: decisión válida procesada y escena mostrada en ≤1 s en ≥95% de ejecuciones | Fluidez de uso / N02 | Estados de una sesión | `src/main.py` — `jugar()` | `scripts/verificar_rnf.py` — `verificar_rnf01_informe()` (N=1000, definición del informe sin cambiar) | `evidencias/verificacion_rnf.txt` (14-10: media 0,592 ms; p95 1,244 ms; máx 4,468 ms; **100% ≤ 1 s → CUMPLE**) |
| RNF-02 Detección del 100% de los errores del conjunto definido | N06 (claridad de errores) | Casos de uso | `src/main.py` — `validar_historia()` | `test_U4_validacion_nueve_categorias` | `evidencias/verificacion_rnf.txt` (RNF-2: 9/9 categorías de la guía) |
| RNF-03 Compatibilidad: dos historias JSON sin modificar el motor | N01 (modificabilidad) | Componentes | `src/main.py` + `data/segunda_historia.json` | `test_RF08_segunda_historia_sin_modificar_el_motor` | `evidencias/verificacion_rnf.txt` (RNF-1) |

## Relación con el cambio solicitado

- Versión anterior al cambio conservada: commit `d146130` (tag `version-pre-cambio`).
- Cambio implementado: commit `41c4686` (tag `version-post-cambio`); requisito en
  `docs/RF-06-deshacer.md`; análisis `evidencias/cambios_antes_despues.diff`.
- Reglas del anexo cubiertas por las pruebas U6 (y variantes), U5 e I1 (§C de
  `docs/AUDITORIA.md`).

## Hallazgos honestos (no ocultados)

1. El informe de Brayan **no vincula sus RF-01..08 con N01–N6** (la guía lo
   exige); el mapeo de la tabla lo hizo Sebastián al construir esta matriz.
2. El informe (§5) sigue citando `data/Historia.json` con mayúscula, ya
   renombrado a `historia.json` (B1). **Hay que actualizar esa referencia en el
   informe antes de entregar.**
3. Los RF-01..05, 07 y 08 del informe no tienen criterios de aceptación
   explícitos (solo RF-06 los tiene en `docs/RF-06-deshacer.md`).
4. **RNF-01 (tiempo de respuesta) está definido pero sin procedimiento ni
   evidencia**; las verificaciones actuales (RNF-1 modificabilidad, RNF-2
   claridad, RNF-3 confiabilidad de `scripts/verificar_rnf.py`) no miden tiempo.
   Decidir: medirlo o sustituir ese RNF por el de modificabilidad ya verificado.
5. El RNF-02 del informe ("100% de un conjunto definido") se adopta aquí como el
   conjunto de las 9 categorías de la guía (verificado 9/9).
6. `evidencias/resultados_pruebas.txt` (UTF-16, Windows de Brayan, 7 pruebas)
   corresponde a una versión anterior: la evidencia vigente es
   `resultados_pruebas_linux.txt` (19/19, UTF-8).

## Evidencia de verificación

Suite completa: **19/19 OK** (`python -m unittest discover -v`), registrada en
`evidencias/resultados_pruebas_linux.txt`. Verificación de RNF:
`evidencias/verificacion_rnf.txt`.

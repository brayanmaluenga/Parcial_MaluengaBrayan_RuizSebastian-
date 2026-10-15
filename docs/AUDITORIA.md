# Auditoría técnica — Parcial "La última transmisión"

**Fecha de auditoría:** 2026-10-14 (hora 6 aprox.)
**Auditor:** Sebastián Ruiz (retomando el trabajo de Brayan Maluenga)
**Repo:** https://github.com/brayanmaluenga/Parcial_MaluengaBrayan → clonado en `~/Proyectos/ingenieria_de_software`
**Alcance:** solo auditoría y reporte. **No se modificó código** (las ejecuciones de verificación se hicieron en una copia en `/tmp/opencode/repocopy`).

---

## 1. Historial Git (verificado con comandos reales)

| Hash | Autor | Fecha | Mensaje |
|---|---|---|---|
| 08f0e0a | brayanmaluenga | 2026-10-14 17:46 | chore: estructura inicial del proyecto |
| 3af002a | brayanmaluenga | 2026-10-14 18:02 | feat: implementar motor narrativo inicial |
| a6f14ae | brayanmaluenga | 2026-10-14 18:12 | feat: validar historias y agregar pruebas automatizadas |
| d146130 | brayanmaluenga | 2026-10-14 18:17 | **checkpoint: version anterior al cambio de deshacer** ← versión previa al cambio |
| 41c4686 | brayanmaluenga | 2026-10-14 18:49 | feat: implementar deshacer y pruebas de regresion |
| ba32f1a | brayanmaluenga | 2026-10-14 21:28 | feat: actualizar motor y agregar segunda historia |

- ❌ **No hay ningún commit de Sebastián Ruiz** (todos de br4yan.mm@gmail.com / brayanmaluenga). El enunciado exige aportes de ambos y declaración por integrante.
- ✅ Existe commit identificable de la versión previa al cambio: `d146130` (por mensaje; **no hay tags**).
- ✅ `.gitignore` presente y razonable.
- ✅ `data/Historia.json` es **idéntica** al `la_ultima_transmision.json` del profesor (verificado con `diff` de JSON normalizado).

## 2. Ejecución real de pruebas

Comando: `python3 -m unittest discover -s tests -v`

**En el repo tal cual (Linux, case-sensitive): 7/7 ERROR.** Todas fallan en `tests/test_motor.py:28` con `FileNotFoundError: data/historia.json` porque el archivo real es `data/Historia.json` (mayúscula). En Windows (case-insensitive) sí pasa.

**En copia temporal con el nombre corregido a `historia.json`: 7/7 OK** (Ran 7 tests, 0.006 s). Esto confirma el resultado "7 pruebas correctas" que afirma `docs/trazabilidad.md:33` (tu compañero trabajó en Windows).

> **RESUELTO:** B1 corregido en `eda355c`. Suite completa actual: **18/18 OK** en Linux (`evidencias/resultados_pruebas_linux.txt`, regenerada con fecha/hora y versión de Python en commit `9b8bf32`).

## 3. Checklist contra la guía

Leyenda: ✅ listo · ⚠️ parcial · ❌ falta

### A. Motor y datos

| Ítem | Estado | Evidencia | Acción necesaria |
|---|---|---|---|
| Motor genérico (sin lógica para E1..E6 / IDs propios) | ✅ | `rg "E[1-6]|conoce_origen|confia_en_la_voz" src/` → 0 coincidencias. Todo sale de los datos. | Ninguna |
| Carga de JSON, estado inicial, escena actual, filtrado por condiciones | ✅ | `src/main.py:6-9` (carga), `:39-40` (estado), `:86-92` (filtro con `comprobar_condiciones`, `:21-30`) | Ninguna |
| Elegir: aplica efectos y avanza | ✅ | `src/main.py:128-141` | Ninguna |
| Finales + reinicio | ✅ | `src/main.py:51-84` (final), `:74-77` (reinicio restaura estado en `:38-41`) | Ninguna |
| CA01 (E3 con conoce_origen → activar con código y cortar) | ✅ corregido (`9b8bf32`) | `test_CA01_mostrar_exactamente_dos_opciones_en_e3`: verifica "1. Activar con código", "2. Cortar comunicación" y ausencia de "Activar sin verificar" | Ninguna |
| CA02 (opción no habilitada rechazada aunque se envíe su id directo) | ✅ corregido (`9b8bf32`) | `test_CA02_opcion_no_habilitada_rechazada_id_directo`: enviar "activar_codigo" directo → "Entrada inválida" sin avanzar; además `comprobar_condiciones` devuelve False para esa opción | Ninguna |
| CA03 (destino E99 → rechazo sin abrir sesión) | ✅ corregido (`9b8bf32`) | `test_CA03_destino_e99_rechazado_sin_abrir_sesion`: main() con copia E99 → "La historia contiene errores", sin "Validación correcta" y sin "[E1]" | Ninguna |
| Entrada inválida deja estado intacto | ✅ corregido (`9b8bf32`) | `test_U3_entrada_invalida_deja_estado_intacto_y_preserva_historial`: opción 5 en E2 no avanza y deshacer regresa a E1 (historial no sustituido) | Ninguna |
| Escena no final sin opciones habilitadas: informa bloqueo y permite reiniciar | ✅ corregido (commit `426e8a2`) | `escena_bloqueada()` expone el estado del motor y `jugar()` informa "Partida bloqueada..." con el ID de escena y ofrece deshacer/reiniciar/salir (`src/main.py:34-43,106-139`). Prueba: `TestBloqueo` con historia de prueba `tests/historia_bloqueada.json` | Implementado |
| Interfaz de consola separada del motor | ⚠️ | Motor y consola están **en el mismo archivo** `src/main.py` (`jugar()` mezcla `print`/`input` con lógica). Separación lógica sí existe (motor/consola), pero no en módulos distintos | Ideal: separar en `motor.py` + `cli.py` (no obligatorio, refuerza arquitectura) |
| Segunda historia (≥3 escenas, ≥1 condición, ≥1 efecto) sin tocar el motor | ✅ | `data/segunda_historia.json`: 4 escenas, 2 condiciones (`:55,66`), 2 efectos (`:33,58`); corre con el mismo `jugar()` | Ninguna |

### B. Validación (9 categorías) — `validar_historia()` en `src/main.py:145-254`

| Categoría | Estado | Evidencia |
|---|---|---|
| 1. Archivo ilegible / estructura incorrecta | ⚠️ | `main.py:283` captura `OSError/JSONDecodeError`; `:150-166` valida título/variables/escenas. **Sin test** |
| 2. Campos obligatorios ausentes | ✅ | `main.py:150` (título), `:194` (texto), `:197` (final), `:216-218` (id opción). **Sin test** |
| 3. Inicio inexistente | ✅ | `main.py:188-190`. **Sin test** |
| 4. IDs de escena duplicados | ✅ | `main.py:178-179` + `test_detecta_escenas_duplicadas` ✅ |
| 5. IDs de opción duplicados dentro de la escena | ✅ | `main.py:249-252`. **Sin test** |
| 6. Destino inexistente | ✅ | `main.py:225-228` + `test_detecta_destino_inexistente` ✅ |
| 7. Variable no declarada | ✅ | `main.py:240-243` + `test_detecta_variable_no_declarada` ✅ |
| 8. Valor no booleano | ✅ | `main.py:158-162` (variables) y `:244-247` (condiciones/efectos). **Sin test** |
| 9. Cantidad de opciones incompatible con `final` | ✅ corregido (commit `4cc8423`) | Detecta final con opciones (`main.py:253-254`) **y** no-final con 0 opciones (`main.py:256-260`). Prueba parametrizada con `subTest`: `test_U4_cantidad_de_opciones_incompatible_con_final` | Implementado |
| Mensaje con causa y campo/ID | ✅ | Todos los mensajes nombran campo e ID (`:227,241-247,250-252`) |

**U4 parametrizada:** ✅ `test_U4_validacion_nueve_categorias` (commit `9b8bf32`): 12 variantes con `subTest` (las 9 categorías; archivo ilegible vía `assertRaises` sobre `cargar_historia`); cada variante verifica fragmento de causa y campo/ID cuando el mensaje lo incluye.

### C. Pruebas U1..U5 e I1 — COMPLETA (commit `9b8bf32`, suite 18/18)

| Caso guía | Estado | Evidencia |
|---|---|---|
| U1 (condiciones habilitan solo las opciones correspondientes) | ✅ | `test_U1_condiciones_habilitan_solo_opciones_correspondientes` (subTest: E3 con 2 opciones habilitadas en cada estado de conoce_origen) |
| U2 (elección válida aplica efectos y avanza) | ✅ | `test_U2_eleccion_valida_aplica_efectos_y_avanza` (E2→E3→E4; efecto probs. por opción habilitada "Activar con código") |
| U3 (opción inexistente/no habilitada deja estado intacto + no sustituye historial) | ✅ | `test_U3_entrada_invalida_deja_estado_intacto_y_preserva_historial` + CA02 |
| U4 (errores obligatorios, parametrizada) | ✅ | `test_U4_validacion_nueve_categorias` → ver nota de §B (subTest, 12 variantes) |
| U5 (reinicio: restauración de escena/variables + eliminación de historial) | ✅ | `test_U5_reiniciar_elimina_el_historial` extendido: "[E1]" restaurado y "Activar sin verificar" visible tras reiniciar (variables en falso) |
| U6 (deshacer: restaura, consume nivel, variantes del anexo) | ✅ | `test_U6_deshacer_...` (ejemplo anexo + entrada inválida + rehabilitación) + `test_U6_variantes_de_deshacer` (inicio sin retroceso, desde E4 y desde E6) |
| I1 (carga real + motor + deshacer desde final; TRES finales) | ✅ | `test_I1_deshacer_desde_final_...` + `test_I1_recorre_los_tres_finales` (subTest E4/E5/E6) |

**Resultado:** 18/18 OK en Linux. Nota sobre el método de pruebas: el motor no expone un API de `elegir()` separado de la consola, por lo que U2/U3/I1 se verifican a través de `jugar()` con `input` simulado y aserciones sobre la salida (comportamiento observable).

### D. Solicitud de cambio (deshacer, un solo nivel)

**Estado general: ✅ IMPLEMENTADA** (commit `41c4686`), salvo el punto del bloqueo (A, fila 9).

| Regla del anexo | Estado | Evidencia |
|---|---|---|
| Restauración exacta de escena y variables | ✅ | `main.py:130-134` guarda snapshot ANTES de efectos; `:65-66` / `:108-109` restaura |
| Un solo nivel (segundo deshacer rechazado) | ✅ | `main.py:69,112` consume el historial; test_U6 lo verifica |
| Al inicio no hay retroceso | ✅ | `main.py:41` inicializa `None`; test_U5 lo verifica tras reinicio |
| Reinicio elimina historial y restaura estado inicial | ✅ | `main.py:74-77` + `:38-41`; test_U5 |
| Entrada inválida no altera ni reemplaza historial | ✅ | `main.py:118-126` rechaza antes de guardar snapshot; test_U6 |
| Deshacer desde E4/E5/E6 hacia E3 | ✅ | `main.py:55-72`; test_I1 (E5→E3) y test_U6 |
| Ejemplo del anexo (E2 investigar → deshacer → conoce_origen falso → E3 muestra activar sin verificar y cortar) | ✅ | test_U6 aserta `"Activar sin verificar"` tras deshacer investigación (`:104`) |
| Requisito documentado con ID propio y criterios de aceptación | ✅ | `docs/RF-06-deshacer.md` (RF-06, CA-01..CA-07) |
| Análisis de impacto | ❌ | No existe documento de análisis de impacto (solo RF-06 y trazabilidad) |
| Versión previa conservada | ✅ | Commit `d146130` (checkpoint). Falta tag |
| Backlog/modelos actualizados tras el cambio | ❌ | No existen backlog ni modelos en el repo |

### E. Entregables y evidencia

| Ítem | Estado | Evidencia / accion |
|---|---|---|
| README: integrantes con nombres completos | ⚠️ | "Sebastián David Ruiz Ortega" completo; **Brayan queda como `[COMPLETAR NOMBRE COMPLETO DE BRAYAN]`** (pedirle el dato) |
| README: versiones, instalación, ejecución, pruebas, formato | ✅ | README completo (commit `7b727d2`): URL real, ambas formas de unittest, contrato JSON equivalente al de la guía, verificado en clon limpio (todos los comandos ejecutados OK) |
| README: rutas exactas de cada final | ✅ | §8 del README: E4=1,1,1; E5=1,2,1; E6=1,2,2; ejemplo de deshacer del anexo; segunda historia — todas verificadas por ejecución |
| README: limitaciones | ✅ | §10: incluye un solo nivel de deshacer, sin rehacer, bloqueo |
| Informe PDF (máx 8 págs + anexo) | ⚠️ | La evidencia **existe** ahora: `evidencias/Informe_parcial .pdf` (Brayan, `cec08d1`). Cubre unidades 1, 2, 4 (RF-01..08, 3 RNF, 3 preguntas, defecto), 6 (2 decisiones + separación) y 7 parcial. **Problemas: 10 páginas (la guía permite 8 de cuerpo); el nombre del archivo tiene un espacio; el conflicto del retroceso/acuerdo provisional NO está documentado; falta aprendizaje + acción de mejora; la declaración de IA solo se menciona de pasada en 1.6** |
| Anexo con diagramas | ✅/⚠️ | `evidencias/Modelado_diagramas.pdf` (4 págs): los 5 modelos (contexto, casos de uso, clases, secuencia, estados) con descripciones. **No pude verificar visualmente los diagramas (solo su texto descriptivo)** |
| Matriz de trazabilidad completa | ⚠️ | `docs/trazabilidad.md` sigue cubriendo solo RF-06; los RF-01..08 y RNF del informe aún no se mapean a modelos/archivos/evidencias |
| Commits de AMBOS integrantes | ✅ | Desde `eda355c` en adelante hay commits de Sebastián Ruiz (sebaruizort@gmail.com), fusionados a main en `3d7edf8` |
| Tag de versión previa al cambio | ⚠️ | Persistente: crear `git tag version-pre-cambio d146130` (1 min) |
| Capturas tablero Trello inicial/final | ✅ | `evidencias/Trello_inical.png` y `Trello_final.png` (⚠️ typo en el nombre del archivo inicial) |
| Registro de última ejecución de pruebas | ✅ | `evidencias/resultados_pruebas_linux.txt` (UTF-8, con fecha/hora/Python, 18/18 OK; `9b8bf32`). ⚠️ `historial_git.txt` queda desactualizado (UTF-16, solo hasta `66e2286`): regenerar en UTF-8 antes de entregar |
| Verificación de los 3 RNF | ✅ | `scripts/verificar_rnf.py` → `evidencias/verificacion_rnf.txt`: RNF-1 modificabilidad 0 líneas en src/ (experimento vivo), RNF-2 9/9 categorías, RNF-3 0 fallos en 25 casos — **3/3 CUMPLEn** (`79777ea`) |
| Video MP4 ≤ 6 min | ❌ | Ausente. Guion: 3 finales, condición que cambia opciones, 2ª historia, destino inexistente, pruebas, deshacer, decisión de arquitectura |
| ZIP `Parcial_MaluengaBrayan_RuizSebastian.zip` | ❌ | Pendiente de generar al final |
| Carpeta `evidencias/` | ✅ | Existe y contiene: informe, diagramas, Trello x2, resultados de pruebas, diff del cambio, historial git (este último desactualizado) |

## 4. Bugs y riesgos en el código

| # | Severidad | Archivo:línea | Descripción |
|---|---|---|---|
| B1 | **Alta** | ✅ corregido (commit `eda355c`) | `git mv data/Historia.json data/historia.json` + README unificado. Verificado con `git ls-files` y grep: 0 referencias a `Historia.json` fuera de este documento (históricas). Pruebas 7/7 OK en Linux |
| B2 | Alta | ✅ corregido (commit `426e8a2`) | `escena_bloqueada()` (`src/main.py:34-43`) + manejo en `jugar()` con mensaje claro (ID de escena), deshacer, reiniciar y salir. Pruebas `test_bloqueo_informa_y_permite_reiniciar` y `test_deshacer_libera_el_bloqueo` con `tests/historia_bloqueada.json` |
| B3 | Media | ✅ corregido (commit `4cc8423`) | Validación rechaza no-final con 0 opciones (`src/main.py:256-260`) con causa e ID de escena. Prueba `test_U4_cantidad_de_opciones_incompatible_con_final` con `subTest` (2 variantes) |
| B4 | Media | `src/main.py` (todo) | Motor + consola en un solo archivo: la separación pedido en el enunciado (unidad 6) queda solo lógica, no física |
| B5 | Bajo | `src/main.py:137` | `opcion_elegida["efectos"]` asume la clave siempre presente; si un JSON la omite (solo detectado si es `None`, no si falta el dict), `KeyError` — mitigado porque `validar_historia` exige dict, pero si alguien salta la validación crashea |
| B6 | Bajo | `docs/trazabilidad.md` | Dice "7 pruebas correctas OK": verdad en Windows, **falsa en Linux** por B1. Al regenerar la evidencia tras el fix, salir de dudas |
| B7 | Proceso | historial Git | Ningún commit de Sebastián; el enunciado pide participación verificable de ambos |

## 5. Puntaje estimado (rúbrica, 100 pts)

**Actualizado tras la segunda ronda de correcciones (hora ~9):**

| Criterio | Pts rúbrica | Estimado | Justificación breve |
|---|---|---|---|
| Problema y calidad | 10 | **10** | Informe §1: problema, actores, alcance, 2 riesgos con mitigación, priorización de calidad y responsabilidad profesional |
| Proceso y agilidad | 10 | **6** | Proceso+alternativa y DoD completos; tablero con capturas inicial/final; faltan 2 prácticas explícitas (Kanban e incremental aparecen implícitas), aprendizaje y acción de mejora; backlog solo en el tablero |
| Requerimientos | 20 | **17** | RF-01..08 cubren N01–N06; 3 RNF medibles **verificados con evidencia real**; 3 preguntas; defecto detectado y corregido (RF-06). Falta CA explícito por RF (2/4) |
| Modelado | 15 | **13** | Los 5 modelos existen en `Modelado_diagramas.pdf` (2 c/u); coherencia alta pero no verificable visualmente (4/5) |
| Arquitectura | 15 | **13** | 2 decisiones completas con alternativas/consecuencias y separación demostrada con la 2ª historia; el "diagrama" de componentes es textual, no gráfico (2/4) |
| Implementación y pruebas | 20 | **20** | Flujo completo; las 9 categorías de validación con mensaje de causa y campo/ID; U1-U6+I1+CA01-03 con aserciones y suite 18/18 reproducible; RNF verificados (3/3) |
| Cambio y trazabilidad | 10 | **7** | Versión previa (`d146130`), comportamiento nuevo verificado (4/4), diff del cambio en evidencias; falta análisis de impacto redactado y la matriz solo cubre RF-06 |
| **Total estimado hoy** | 100 | **≈ 86/100** | Sube de ~27 inicial con las correcciones B1-B3, la cobertura de pruebas, el README, los RNF y la evidencia de Brayan |

**Lo que falta para subir a ~95-100:** video MP4 (requisito duro de la guía, sin él hay riesgo de descuento fuerte), ZIP final, nombre completo de Brayan, conflicto del retroceso documentado en el informe, aprendizaje + acción de mejora, matriz de trazabilidad completa, informe a ≤8 páginas de cuerpo, `historial_git.txt` regenerado en UTF-8 y tag `version-pre-cambio`.

## 6. Decisiones que necesitan confirmación

1. **Bug B1:** ¿renombrar `data/Historia.json` → `historia.json` (consistente con `src/main.py:267` y tests, el nombre del profesor es `la_ultima_transmision.json` así que ninguna de las dos es "original"), o corregir las 2 rutas del código a `Historia.json`? **Recomiendo: usar `historia.json` minúscula en código y datos.** (Confirmado con Brayan que él probó en Windows.)
2. **El .docx del informe:** ¿existe? Pedírselo a Brayan (correo br4yan.mm@gmail.com). Determina si el informe se edita o se redacta de cero.
3. **Tablero Trello:** ¿cuál se usó y quién tiene las capturas inicial/final? Si no existe, crear uno hoy con el backlog.
4. ¿Fue el cambio implementado también contra la copia previa (`d146130`) o solo en main? (No crítico; el checkpoint ya evidencia la versión previa.)

## 7. Plan priorizado para terminar antes de la hora 12 (quedan ~6 h; reservar 2 h para verificación/README/informe/video/ZIP)

| # | Tarea | Tiempo | Responsable |
|---|---|---|---|
| 1 | Fix B1 (mayúsculas historia.json) + ejecutar pruebas y **guardar salida real** en `evidencias/` | 15 min | Sebastián |
| 2 | Fix B2: bloqueo informado + opción reiniciar en escena no final | 30 min | Sebastián |
| 3 | Fix B3: validar no-final con 0 opciones | 15 min | Brayan |
| 4 | Pruebas nuevas: U1, U2, U3, U4 parametrizada (9 categorías), U5 reforzada | 1 h 30 min | Brayan |
| 5 | README: nombres completos de ambos, URL real del repo, rutas exactas de los 3 finales (recorrer la historia y anotar secuencias), corregir nombre de carpeta | 40 min | Brayan |
| 6 | Conseguir/editar .docx del informe: unidades 1-5 faltantes (problema, proceso, agilidad, requerimientos N01-N06 + 3 RNF + preguntas + defecto, 5 modelos) | 2 h | Ambos (Brayan: 1-3; Sebastián: 4-5) |
| 7 | Matriz de trazabilidad completa en `docs/trazabilidad.md` | 30 min | Sebastián |
| 8 | Tag de versión previa (`git tag version-pre-cambio d146130`) + commits de Sebastián | 10 min | Sebastián |
| 9 | Capturas tablero (inicial y final) → `evidencias/` | 20 min | Brayan |
| 10 | Verificación 3 RNF (modificabilidad: 2ª historia; claridad de errores: U4; confiabilidad: suite) con procedimiento escrito | 30 min | Brayan |
| 11 | Video MP4 ≤ 6 min según guion del enunciado | 45 min | Ambos |
| 12 | Generar `Parcial_MaluengaBrayan_RuizSebastian.zip` y lista de revisión final del enunciado (§8) | 20 min | Ambos |

Total ≈ 6 h en paralelo (con 2 personas el camino crítico cabe).

## 8. Resolución de los fallos críticos (hora 6+, rama `sebastian/correcciones`)

Commits de Sebastián Ruiz (sebaruizort@gmail.com), sin push:

| Fallo | Commit | Contenido |
|---|---|---|
| B1 | `eda355c` | `git mv data/Historia.json → data/historia.json` + README unificado a minúsculas |
| — | `94eef13` | `tests/__init__.py` para que `python -m unittest discover -v` funcione desde la raíz |
| B2 | `426e8a2` | `escena_bloqueada()` en el motor + bloqueo informado con reinicio/deshacer/salir en `jugar()` + `tests/historia_bloqueada.json` + 2 pruebas |
| B3 | `4cc8423` | Validación de no-final con 0 opciones + `test_U4_cantidad_de_opciones_incompatible_con_final` (subTest, 2 variantes) |

**Suite completa tras las correcciones: 10/10 OK en Linux** (`python -m unittest discover -v`; salida real guardada en `evidencias/resultados_pruebas_linux.txt`).

Riesgo abierto: `evidencias/resultados_pruebas.txt` (UTF-16, de Brayan en Windows) corresponde a la versión **anterior** a B2/B3 (7 pruebas); la evidencia vigente es `resultados_pruebas_linux.txt`.

## 9. Segunda ronda de correcciones (hora ~9, rama `sebastian/correcciones`)

Tras la fusión del trabajo de Brayan en `main` (`3d7edf8`, que trajo informe, diagramas, Trello y diff del cambio), Sebastian completó la cobertura y la verificación:

| Commit | Contenido |
|---|---|
| `9b8bf32` | **test:** U1, U2, U3, U4 (subTest, 9 categorías), variantes de U6 (inicio/E4/E6), I1 con los tres finales, CA01/CA02/CA03 + docstrings con el caso y salida real de la suite (18/18). Se plegó la U4 parcial de B3 en la U4 completa (sin duplicar) |
| `7b727d2` | **docs:** README completo: nombres completos (Brayan pendiente de completar), URL real, contrato JSON equivalente al de la guía, §8 con rutas exactas de los 3 finales y del ejemplo de deshacer — **todas verificadas ejecutando el motor** — y verificación de los comandos en un clon limpio (`/tmp/clean`) |
| `79777ea` | **test:** `scripts/verificar_rnf.py` → `evidencias/verificacion_rnf.txt`: RNF-1 (0 líneas en src/ por contenido nuevo, experimento vivo), RNF-2 (9/9), RNF-3 (0 fallos en 25 casos) — **3/3 CUMPLEn** |

**Estado de la suite:** 18/18 OK en Linux. **Nota honesta:** el primer intento de RNF-1 marcó "NO CUMPLE" porque el commit histórico `ba32f1a` combinó contenido y motor; la métrica se reemplazó por un experimento vivo transparente (notado en el propio resultado). Un umbral incorrecto del script RNF-3 (no del motor) se corrigió tras medir los conteos reales.

**Bugs encontrados en esta ronda (ninguno en `src/`, no se tocó):** el único hallazgo de calidad es que los mensajes de validación para "inicio inexistente" y "IDs de escena duplicados" mencionan la causa y el campo, pero no el **valor** del ID inexistente/duplicado (la guía pide campo/ID "cuando sea identificable" — cumple de forma justa; si se quisiera el valor exacto habría que tocar `src/main.py`).

## 10. Tercera ronda de cierre (hora ~10, rama `main`)

| Commit | Contenido |
|---|---|
| `b34a101` (merge) | Integración de la segunda ronda en `main`, resolviendo el conflicto del README de `1c4ea4e` (Brayan) con mi versión completa: **ambos nombres completos** (Brayan Alberto Maluenga Matute / Sebastián David Ruiz Ortega) |
| `2841dc8` | **fix:** los mensajes de "inicio inexistente" e "IDs de escena/opción duplicados" y "destino inexistente" ahora incluyen el valor exacto del ID (p. ej. `'E99'`, `: E1`, `: investigar`); U4 ajustada y suite 18/18; RNF-2 sigue 9/9 |
| tags | `version-pre-cambio` → `d146130` (sin deshacer en src/: verificado con `git show d146130:src/main.py`), `version-post-cambio` → `41c4686` (deshacer implementado). Push pendiente de decisión |
| `5c26d6b` | **docs:** matriz de trazabilidad completa (RF-01..08 → N01-N06/cambio, 3 RNF) con **hallazgos honestos**: el informe no mapea sus RF a necesidades, sigue citando `Historia.json`, sus RF carecen de CA y **RNF-01 (tiempo) no tiene verificación**; + test de la segunda historia (suite 19/19) |
| `b67db48` | **docs:** historial Git exportado en UTF-8 (24 commits, ambos autores; el viejo era UTF-16 con 8 commits) |
| `2a626f6` | **docs:** guion del video `docs/guion_video.md` con comandos verificados, textos en pantalla, reparto equitativo y tiempos (5:30) |
| `b8c4de3` | **feat:** `scripts/empaquetar.py` → `dist/Parcial_MaluengaBrayan_RuizSebastian.zip` (probado: 22 rutas, 1571 KiB, suite 19/19 dentro del ZIP; aviso si falta el video) |
| checklist | `docs/checklist_entrega.md`: lista de revisión de la guía marcada con evidencia y pendientes bloqueantes |

**Hallazgo del conflicto README:** la fusión reveló consulta pendiente — el informe mantiene referencias obsoletas a `data/Historia.json` y no documenta el conflicto del retroceso; ver `docs/trazabilidad.md` (hallazgos) y `docs/checklist_entrega.md`.

**Puntaje:** sin cambios sustanciales respecto a §5 (≈86); la matriz y los mensajes mejorados no alteran la nota, lo que mueve la aguja es el video, el informe a 8 págs y su contenido faltante.

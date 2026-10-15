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

> El fix es una línea (renombrar el archivo de datos o corregir las 2 rutas en `tests/test_motor.py:24-27` y `src/main.py:267`). **Pendiente de decisión** (ver §6).

## 3. Checklist contra la guía

Leyenda: ✅ listo · ⚠️ parcial · ❌ falta

### A. Motor y datos

| Ítem | Estado | Evidencia | Acción necesaria |
|---|---|---|---|
| Motor genérico (sin lógica para E1..E6 / IDs propios) | ✅ | `rg "E[1-6]|conoce_origen|confia_en_la_voz" src/` → 0 coincidencias. Todo sale de los datos. | Ninguna |
| Carga de JSON, estado inicial, escena actual, filtrado por condiciones | ✅ | `src/main.py:6-9` (carga), `:39-40` (estado), `:86-92` (filtro con `comprobar_condiciones`, `:21-30`) | Ninguna |
| Elegir: aplica efectos y avanza | ✅ | `src/main.py:128-141` | Ninguna |
| Finales + reinicio | ✅ | `src/main.py:51-84` (final), `:74-77` (reinicio restaura estado en `:38-41`) | Ninguna |
| CA01 (E3 con conoce_origen → activar con código y cortar) | ✅ | flujo del motor + `data/Historia.json:50-82`; implícito en test_U6/I1 | Falta test explícito U1/CA01 |
| CA02 (opción no habilitada rechazada aunque se envíe su id directo) | ⚠️ | Por diseño el motor solo acepta índices de la lista filtrada (`main.py:124-128`); **no hay API** para pasar id directo, pero **no hay test** que lo demuestre | Añadir aserción en U2/U3 |
| CA03 (destino E99 → rechazo sin abrir sesión) | ⚠️ | `validar_historia` lo detecta (`main.py:225-228`) y `main()` valida antes de `jugar` (`:272-281`); test `test_detecta_destino_inexistente` existe pero **no verifica "sin abrir sesión"** | Añadir test (cae dentro de U4) |
| Entrada inválida deja estado intacto | ✅ | `main.py:118-126` (rechaza antes de tocar `historial_deshacer`/variables); cubierto dentro de test_U6 (`"99"`) | Test U3 explícito falta |
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

**U4 parametrizada:** ❌ No existe ninguna prueba parametrizada (`rg "subTest|paramet" tests/` → 0).

### C. Pruebas U1..U5 e I1

| Caso guía | Estado | En `tests/test_motor.py` | Acción |
|---|---|---|---|
| U1 (condiciones habilitan solo las opciones correspondientes) | ❌ | No hay test con ese nombre ni aserción directa | Crear (~20 min) |
| U2 (elección válida aplica efectos y avanza) | ❌ | Implícito en U6/I1 pero sin aserción directa de efectos | Crear (~20 min) |
| U3 (opción inexistente/no habilitada deja estado intacto) | ⚠️ | Cubierto de pasada en test_U6 (`"99"` + mensaje), sin test propio | Crear (~20 min) |
| U4 (errores obligatorios, parametrizada) | ❌ | Solo 3 variantes sueltas (`:34-66`), sin `subTest` | Crear parametrizada (~40 min) |
| U5 (reinicio; versión extendida: elimina historial) | ⚠️ | `test_U5_reiniciar_elimina_el_historial` (`:106-123`) ✅ extended OK, pero **no aserta restauración de escena/variables iniciales** | Completar (~15 min) |
| U6 (deshacer: restaura, consume nivel, entrada inválida preserva, nueva elección re-habilita) | ✅ | `test_U6_deshacer_restaurar_estado_y_consumir_historial` (`:69-104`), con variantes del anexo | Ninguna |
| I1 (carga real + motor hasta un final; extendida con deshacer desde final) | ✅ | `test_I1_deshacer_desde_final_con_historia_cargada` (`:126-141`) | Ninguna |

**Resultado:** 7/7 pasan (con fix de mayúsculas). Faltan U1, U2, U3, U4-parametrizada y el refuerzo de U5.

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
| README: integrantes con nombres completos | ❌ | `README.md:6-10` solo lista "Brayan Maluenga" (sin nombre completo ni a Sebastián) |
| README: versiones, instalación, ejecución, pruebas, formato | ✅/⚠️ | `README.md:10-17,52-105,126-153`. ⚠️ instalación usa placeholder `URL_DEL_REPOSITORIO` (`:56`) y habla de carpeta `La-Ultima-Transmision/` (`:29,60`) que no coincide con el repo |
| README: rutas exactas de cada final | ❌ | `README.md:157-167` lo deja "para completar después" — sin secuencias de decisión |
| README: limitaciones | ✅ | `README.md:193-201` |
| Informe PDF (máx 8 págs + anexo) | ❌ | No existe en el repo. **El .docx del compañero NO está en `docs/enunciado/` ni en ninguna parte del sistema** (buscado sin éxito). **No puedo verificar su contenido; hay que pedirle a Brayan el .docx.** |
| Secciones informe por unidad (1-7) | ❌/no verificable | No verificable sin el .docx. En el repo solo existe contenido de la unidad 7 parcial (bibliotecas y licencias en `README.md:203-213`) y el cambio (unidad de gestión de cambio: RF-06 + trazabilidad parcial) |
| Matriz de trazabilidad completa (RF/RNF → modelos → archivos → evidencia) | ⚠️ | `docs/trazabilidad.md` existe pero **solo cubre RF-06 del cambio**; no hay RF propios N01-N06 ni RNF ni modelos que trazar |
| Commits de AMBOS integrantes | ❌ | Solo Brayan. **Sebastián debe hacer commits con su nombre/email configurados** |
| Tag de versión previa al cambio | ⚠️ | No hay tag; solo el mensaje del commit `d146130`. Crear `git tag` es 1 min |
| Capturas tablero Trello inicial/final | ❌ | Ausentes (no hay carpeta `evidencias/`; el README no la menciona en realidad — la mención estaba prevista pero no está) |
| Registro de última ejecución de pruebas | ⚠️ | `docs/trazabilidad.md:33` afirma "7 pruebas correctas (OK)" pero **no hay archivo con la salida real**, y en Linux no se reproduce (bug mayúsculas) |
| Verificación de los 3 RNF | ❌ | No hay RNF definidos ni verificación |
| Video MP4 ≤ 6 min | ❌ | Ausente. Guion exigido: 3 finales, condición que cambia opciones, 2ª historia, error destino inexistente, pruebas, deshacer, decisión de arquitectura |
| ZIP `Parcial_MaluengaBrayan_RuizSebastian.zip` | ❌ | Pendiente de generar al final |
| Carpeta `evidencias/` | ❌ | No existe en el repo |

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

Con **solo lo verificable en el repo hoy**:

| Criterio | Pts rúbrica | Estimado | Justificación breve |
|---|---|---|---|
| Problema y calidad | 10 | **0** | Nada de problema/actores/alcance/riesgos/responsabilidad profesional en el repo |
| Proceso y agilidad | 10 | **0** | Sin backlog, tablero, prácticas, DoD ni aprendizaje |
| Requerimientos | 20 | **2** | Solo RF-06 con criterios de aceptación (4 pts de CA parcial); no hay RF N01-N06, ni RNF, ni preguntas, ni defecto documentado |
| Modelado | 15 | **0** | Sin los 5 modelos |
| Arquitectura | 15 | **5** | Sin diagrama ni decisiones documentadas (0 de 10), pero la separación contenido/motor/interfaz está demostrada con la 2ª historia (5/5) |
| Implementación y pruebas | 20 | **13** | Flujo 6/6; validaciones ~3/4 (falta categoría 9); U1-U5+I1 ~3/6 (solo U5, U6, I1); ejecución reproducible 1/2 (bug B1); RNF 0/2 |
| Cambio y trazabilidad | 10 | **7** | Versión previa ✅ (2), comportamiento + pruebas ✅ (4), artefactos/trazabilidad ~1/4 (trazabilidad solo del cambio) |
| **Total estimado hoy** | 100 | **≈ 27/100** | |

⚠️ **Advertencia importante:** si el .docx del compañero (que no encuentro en el sistema) ya contiene unidades 1-5, el puntaje potencial sube a ~70-80. **Primer paso: conseguir ese .docx.** Si no existe, hay que redactar todo el informe desde cero.

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

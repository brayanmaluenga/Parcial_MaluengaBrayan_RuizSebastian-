# Declaración de aportes por integrante

Fuente única y verificable: `git log --all --format='%h | %an | %ad | %s'`
(congelado en `evidencias/historial_git.txt`). Solo se afirma lo que muestra
el historial; lo que no está en Git se marca aparte al final.

## Resumen

| Autor (cuenta Git / persona) | Commits | Período | Tipos de trabajo |
|---|---|---|---|
| brayanmaluenga (Brayan Alberto Maluenga Matute) | 10 | 2026-10-14 17:46 → 22:03 | Motor inicial, historias de datos, validación, deshacer, demostración, fixtures de evidencia |
| Sebastián Ruiz (Sebastián David Ruiz Ortega) | 19 | 2026-10-14 21:44 → 22:2x | Auditoría, corrección de bugs, cobertura de pruebas, verificación de RNF, README, trazabilidad, empaquetado y cierre |

## Brayan Alberto Maluenga Matute — 10 commits

| Commit | Tema | Archivos principales |
|---|---|---|
| `08f0e0a` | chore: estructura inicial del proyecto | README, .gitignore, estructura |
| `3af002a` | feat: motor narrativo inicial | `src/main.py` |
| `a6f14ae` | feat: validar historias + pruebas automatizadas | `src/main.py`, `tests/test_motor.py` |
| `d146130` | checkpoint: versión anterior al cambio | — (tag `version-pre-cambio`) |
| `41c4686` | feat: deshacer + pruebas de regresión | `src/main.py` (+127/-43), `tests/`, `docs/RF-06-deshacer.md`, `docs/trazabilidad.md` |
| `ba32f1a` | feat: segunda historia + actualización del motor | `data/segunda_historia.json`, `src/main.py` |
| `426db53` | docs: README | README |
| `66e2286` | test: registrar resultados (Windows) | `evidencias/resultados_pruebas.txt` (UTF-16, hoy desactualizado) |
| `cec08d1` | docs: evidencias del parcial | informe PDF, diagramas PDF, Trello PNG ×2, diff del cambio, historial |
| `1c4ea4e` | docs: README con nombres completos | README |

## Sebastián David Ruiz Ortega — 19 commits

| Commit | Tema | Archivos principales |
|---|---|---|
| `eda355c` | fix: renombrar historia.json (B1, fallas en Linux) | `data/historia.json` (git mv), README |
| `94eef13` | test: descubrir pruebas desde la raíz | `tests/__init__.py` |
| `426e8a2` | fix: bloqueo de escena sin opciones (B2) | `src/main.py` (`escena_bloqueada`), `tests/historia_bloqueada.json`, 2 pruebas |
| `4cc8423` | fix: no-final con 0 opciones (B3) | `src/main.py` (validación), prueba subTest |
| `249268a` | docs: auditoría B1-B3 | `docs/AUDITORIA.md` |
| `9b8bf32` | test: cobertura U1-U4, U6/I1 variantes, CA01-03 | `tests/test_motor.py` (+108), `evidencias/resultados_pruebas_linux.txt` |
| `7b727d2` | docs: README completo + rutas de finales verificadas | README |
| `79777ea` | test: verificación de RNF-A/B/C | `scripts/verificar_rnf.py`, `evidencias/verificacion_rnf.txt` |
| `5caad4a` | docs: auditoría segunda ronda (puntaje 86/100) | `docs/AUDITORIA.md` |
| `3d7edf8`, `b34a101` | merges de integración (incluida la resolución del conflicto README con los nombres completos) | README + árbol integrado |
| `2841dc8` | fix: IDs exactos en mensajes de validación | `src/main.py`, `tests/`, `scripts/`, evidencias |
| `5c26d6b` | docs: matriz de trazabilidad completa + test 2ª historia | `docs/trazabilidad.md`, `tests/test_motor.py` |
| `b67db48` | docs: historial Git en UTF-8 | `evidencias/historial_git.txt` |
| `2a626f6` | docs: guion del video | `docs/guion_video.md` |
| `d5b2fd5` | test: RNF-01 del informe (tiempo, N=1000) | `scripts/verificar_rnf.py`, evidencias |
| `b8c4de3` | feat: empaquetador del ZIP | `scripts/empaquetar.py`, `.gitignore` |
| `7ebd35e` | docs: checklist de entrega + cierre auditoría | `docs/checklist_entrega.md` |
| `2cd8515` | fix: .gitignore | `.gitignore` |

## Partes NO atribuibles por Git (se atribuyen por declaración del equipo)

El commit `cec08d1` muestra que **el archivo fue subido por brayanmaluenga**,
pero Git no registra quién elaboró su contenido ni el trabajo del tablero:

1. `evidencias/Informe_parcial .pdf` (informe, secciones 1-5) — fuera de Git.
2. `evidencias/Modelado_diagramas.pdf` (los 5 modelos) — fuera de Git.
3. Tablero Trello (backlog, responsables, evolución; capturas `Trello_inical.png`
   —sic— y `Trello_final.png`) — el tablero vive en Trello, no en Git.
4. La captura del video cuando se grabe y el guion de reparto de voz no pueden
   verificarse por historial.

**Evidencia sugerida para el informe:** completar esta tabla con la
confirmación explícita de ambos integrantes (quién redactó el informe, quién
hizo los diagramas, quién administró el Trello) antes de generar el ZIP final.
Git solo acredita que `cec08d1` (subida de esos archivos) es de brayanmaluenga.

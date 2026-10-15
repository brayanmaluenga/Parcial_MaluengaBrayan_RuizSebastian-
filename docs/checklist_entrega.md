# Lista de revisión antes de entregar (sección 8 de la guía)

Fecha: 2026-10-14 (hora ~10). ✅ = verificado · ⚠️ = parcial · ❌ = pendiente

| # | Requisito de la guía | Estado | Evidencia |
|---|---|---|---|
| 1 | La solución puede instalarse y ejecutarse siguiendo únicamente el README | ✅ | Verificado en clon limpio: `git clone . /tmp/clean` + cada comando del README (motor, ambas formas de unittest, py_compile, json.tool). Resultados en `docs/AUDITORIA.md` §3 y en la sesión de verificación |
| 2 | Los tres finales son alcanzables y las opciones dependen del estado | ✅ | `tests/test_motor.py::test_I1_recorre_los_tres_finales` (E4/E5/E6); rutas exactas en README §8 (verificadas ejecutando); CA01/CA02 |
| 3 | La segunda historia funciona sin modificar el código del motor | ✅ | `test_RF08_segunda_historia_sin_modificar_el_motor`; `scripts/verificar_rnf.py` RNF-1 (0 líneas en src/) → `evidencias/verificacion_rnf.txt` |
| 4 | Los errores obligatorios producen respuestas controladas y comprensibles | ✅ | `test_U4_validacion_nueve_categorias` (12 variantes, subTest) + RNF-2 9/9 con causa y campo/ID |
| 5 | La solicitud de cambio está implementada y cubierta por pruebas | ✅ | RF-06 en `docs/RF-06-deshacer.md`; tags `version-pre-cambio` (d146130) y `version-post-cambio` (41c4686); U6 + variantes, U5, I1, bloqueo; suite 19/19 OK |
| 6 | Los requisitos, modelos y matriz corresponden a la versión entregada | ✅/⚠️ | Matriz completa en `docs/trazabilidad.md`; modelos en `evidencias/Modelado_diagramas.pdf`. ⚠️ El informe §5 aún cita `data/Historia.json` (renombrada a `historia.json`) — actualizarlo en Brayan |
| 7 | Se incluyeron resultados reales, fuentes y aportes de ambos integrantes | ⚠️ | Resultados reales: `evidencias/resultados_pruebas_linux.txt` (19/19) y `evidencias/verificacion_rnf.txt`. Aportes: commits de ambos autores (`evidencias/historial_git.txt`). ⚠️ **Falta la declaración explícita de uso de IA y fuentes en el informe** (el §1.6 la menciona solo de pasada) |
| 8 | El ZIP, el informe, el anexo y el video o su enlace abren correctamente | ⚠️ | Informe y anexo: PDFs válidos (`evidencias/Informe_parcial .pdf`, `Modelado_diagramas.pdf`). ZIP: `scripts/empaquetar.py` probado (19/19 dentro del ZIP) pero el ZIP final se genera al cierre. ❌ **Video MP4 ausente** — guion listo en `docs/guion_video.md` |

## Pendientes bloqueantes antes del cierre (hora 12)

1. ❌ **Grabar el video MP4 ≤ 6 min** siguiendo `docs/guion_video.md` y guardarlo en `evidencias/demostracion.mp4` (o enlazarlo). Es requisito duro de la guía.
2. ❌ **Regenerar el ZIP final** con `python scripts/empaquetar.py` ya con el video dentro y verificar que abre.
3. ⚠️ **Ajustar el informe:** bajar a ≤ 8 págs de cuerpo (tiene 10), actualizar `Historia.json` → `historia.json`, añadir el conflicto del retroceso/acuerdo provisional documentado, un aprendizaje con acción de mejora (unidad 3) y la declaración de IA y fuentes.
4. ⚠️ **RNF-01 del informe (tiempo de respuesta) sin verificación** — decidir: medirlo o sustituirlo por el RNF de modificabilidad ya verificado (ver hallazgos en `docs/trazabilidad.md`).
5. ⚠️ Push de los tags cuando se decida: `git push origin version-pre-cambio version-post-cambio`.

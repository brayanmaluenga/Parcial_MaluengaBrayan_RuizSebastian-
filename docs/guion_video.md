# Guion de demostración (video MP4 ≤ 6 min, sin cámara)

**Duración total: 5:30 de contenido + 0:30 de margen.** Cada escena indica el
comando exacto (verificado en este repo), el texto que debe verse en pantalla y
quién habla. Se puede explicar con voz o rótulos; el texto en pantalla debe ser
legible. Gravar la terminal con la fuente agrandada (`Ctrl`+`+`).

Grabación sugerida: OBS o `ffmpeg -f x11grab`; exportar MP4 y guardarlo como
`evidencias/demostracion.mp4` (o subirlo y enlazarlo desde el README).

---

## Escena 1 — Presentación (0:00 → 0:30)

- **En pantalla:** terminal con el repo abierto (`ls`, `git log --oneline -5`).
- **Rótulo:** "La última transmisión — motor de historias interactivas".
- **Hablan (15 s cada uno, 30 s total):**
  - Sebastián: "Somos Sebastián Ruiz y Brayan Maluenga; en 6 minutos: los finales, el motor con segunda historia, la validación de errores, las pruebas y el deshacer solicitado a la hora 6."
- **Comando:**
  ```bash
  git log --oneline -5
  ```

## Escena 2 — Tres finales y una condición que cambia las opciones (0:30 → 1:45)

- **Habla:** Sebastián (75 s).
- **Comandos y texto a mostrar:**
  1. Final E4:
     ```bash
     printf '1\n1\n1\ns\n' | python src/main.py data/historia.json
     ```
     Se ve: `[E1]`, `[E2]`, opción "Activar con código" y `[E4] Rescate` → `Fin de la transmisión.`
  2. Final E5:
     ```bash
     printf '1\n2\n1\ns\n' | python src/main.py data/historia.json
     ```
     Se ve: en `[E3]` aparecen "Activar sin verificar" y "Cortar comunicación" ( **condición** : `conoce_origen` es falso porque no se investigó).
  3. Final E6:
     ```bash
     printf '1\n2\n2\ns\n' | python src/main.py data/historia.json
     ```
     Se ve: `[E6] Silencio`.
- **Qué decir:** "Las condiciones habilitan solo las opciones compatibles: al investigar el archivo, E3 ofrece 'Activar con código'; sin investigar, esa opción desaparece — el motor evalúa las reglas desde los datos, sin lógica especial para las escenas".

## Escena 3 — Segunda historia con el mismo motor (1:45 → 2:25)

- **Habla:** Brayan (40 s).
- **Comando:**
  ```bash
  printf '1\n1\n1\ns\n' | python src/main.py data/segunda_historia.json
  ```
- **Se ve:** título "La señal del refugio", escenas `[E1]..[E4]` y su final propio.
- **Qué decir:** "Una historia distinta, con otras variables y condiciones (`codigo_verificado`, `rescate_enviado`), corre con el mismo motor: cero líneas de código cambiadas".

## Escena 4 — Error de destino inexistente (CA03) (2:25 → 3:05)

- **Habla:** Brayan (40 s).
- **Comando:**
  ```bash
  python3 -c "import json, pathlib; h=json.load(open('data/historia.json')); h['escenas'][0]['opciones'][0]['destino']='E99'; pathlib.Path('/tmp/historia_e99.json').write_text(json.dumps(h, ensure_ascii=False))" && python src/main.py /tmp/historia_e99.json
  ```
- **Se ve (literal):**
  ```
  La historia contiene errores:
  - El destino 'E99' de la opción 'revisar' no existe.
  ```
- **Qué decir:** "El contenido con un destino roto se rechaza con un mensaje que nombra el campo y el ID, y nunca se abre una sesión jugable".

## Escena 5 — Pruebas automatizadas (3:05 → 3:45)

- **Habla:** Sebastián (40 s).
- **Comando:**
  ```bash
  python -m unittest discover -v
  ```
- **Se ve:** `Ran 19 tests ... OK` (U1–U6, I1, CA01–CA03, bloqueo y RNF).
- **Qué decir:** "Cobertura de los casos de la guía y del anexo, con aserciones; la evidencia real está en evidencias/resultados_pruebas_linux.txt".

## Escena 6 — Deshacer (3:45 → 4:45)

- **Hablan:** Brayan (ejemplo del anexo, 30 s) y Sebastián (desde un final, 30 s).
- **6a. Ejemplo del anexo (Brayan):**
  ```bash
  printf '1\n1\nd\nd\n2\n1\ns\n' | python src/main.py data/historia.json
  ```
  Se ve: en `[E3]` escribir `d` → "Decisión deshecha." y regreso a `[E2]` con `conoce_origen` false; segundo `d` → "No hay ninguna decisión para deshacer."; luego `2` vuelve a `[E3]` mostrando "Activar sin verificar" y "Cortar comunicación".
  - Qué decir: "Deshacer restaura escena y variables exactas y consume el retroceso: un solo nivel".
- **6b. Desde un final (Sebastián):**
  ```bash
  printf '1\n1\n1\nd\n2\n1\ns\n' | python src/main.py data/historia.json
  ```
  Se ve: llegar a `[E4]`, `d` → "Decisión deshecha." y regreso a `[E3]` con los valores previos; luego "Cortar" lleva a `[E6]`.
  - Qué decir: "El retroceso funciona también desde los finales E4, E5 y E6, y una nueva elección vuelve a habilitarlo una sola vez".

## Escena 7 — Decisión de arquitectura e impacto del cambio (4:45 → 5:30)

- **En pantalla:** `Modelado_diagramas.pdf` (diagrama de componentes) junto al terminal con el diff.
- **Habla:** Brayan (45 s).
- **Comando:**
  ```bash
  git show --stat 41c4686 | head -12
  ```
- **Se ve:** las 4 rutas tocadas por el cambio (motor, pruebas, RF-06, trazabilidad).
- **Qué decir:** "Decisión clave: separar contenido (JSON), motor e interfaz; por eso el deshacer se implementó solo en el motor y su interfaz, sin tocar historia.json — impacto: 4 archivos, trazables con `evidencias/cambios_antes_despues.diff`".

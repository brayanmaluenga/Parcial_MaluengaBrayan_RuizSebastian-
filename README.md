
# La última transmisión

Motor narrativo interactivo desarrollado en Python. Permite ejecutar historias almacenadas en archivos JSON, tomar decisiones, modificar variables y llegar a diferentes finales.

## 1. Integrantes

- Sebastián David Ruiz Ortega
- [COMPLETAR NOMBRE COMPLETO DE BRAYAN] (Brayan Maluenga)

## 2. Versiones requeridas

- Sistema operativo: Windows 10/11 o compatible con Python.
- Python: 3.10 o superior como referencia.
- Git: para el control de versiones.
- Visual Studio Code: editor recomendado.

El proyecto utiliza módulos de la biblioteca estándar de Python: `json`, `pathlib`, `sys` y `unittest`. No requiere instalar paquetes externos para las funcionalidades descritas.

Para consultar las versiones instaladas:

```bash
python --version
git --version
```

## 3. Estructura del proyecto

```text
Parcial_MaluengaBrayan/
├── data/
│   ├── historia.json
│   └── segunda_historia.json
├── docs/
│   ├── RF-06-deshacer.md
│   ├── trazabilidad.md
│   └── AUDITORIA.md
├── evidencias/
├── src/
│   └── main.py
├── tests/
│   ├── historia_bloqueada.json
│   └── test_motor.py
├── .gitignore
└── README.md
```

- `src/main.py`: contiene el motor narrativo.
- `data/historia.json`: contiene la historia original.
- `data/segunda_historia.json`: contiene una segunda historia.
- `tests/test_motor.py`: contiene las pruebas automatizadas.
- `docs/RF-06-deshacer.md`: documenta el requisito de deshacer.
- `docs/trazabilidad.md`: relaciona los requisitos con la implementación.
- `README.md`: contiene la documentación del proyecto.

## 4. Instalación

### Clonar el repositorio

```bash
git clone https://github.com/brayanmaluenga/Parcial_MaluengaBrayan.git
cd Parcial_MaluengaBrayan
```

Si ya tienes el proyecto descargado, abre la carpeta en Visual Studio Code y selecciona **Terminal > Nueva terminal**.

Comprueba que Python esté instalado:

```bash
python --version
```

No necesitas instalar dependencias externas si el proyecto utiliza únicamente los módulos estándar indicados.

## 5. Comandos de ejecución

### Ejecutar la historia original

```bash
python src/main.py data/historia.json
```

### Ejecutar la segunda historia

```bash
python src/main.py data/segunda_historia.json
```

### Comprobar la sintaxis de Python

```bash
python -m py_compile src/main.py
```

### Validar el formato JSON de la historia original

```bash
python -m json.tool data/historia.json
```

### Validar el formato JSON de la segunda historia

```bash
python -m json.tool data/segunda_historia.json
```

La validación sintáctica de JSON no garantiza que todos los destinos y variables sean correctos. Para ello también se utiliza la validación del motor narrativo.

## 6. Pruebas automatizadas

Ejecuta las pruebas con cualquiera de estos dos comandos equivalentes:

```bash
python -m unittest discover -v
```

```bash
python -m unittest discover -s tests -v
```

La suite cubre los casos de la guía (U1 a U6, I1 y CA01 a CA03), el bloqueo
de escenas sin opciones habilitadas y las variantes de deshacer del anexo.
Cada prueba documenta su caso en el docstring; las parametrizadas usan
`subTest`.

Las pruebas deben ejecutarse después de realizar cambios importantes. Los
resultados incluidos en la entrega corresponden a una ejecución real
(`evidencias/resultados_pruebas_linux.txt`).

## 7. Formato del contenido narrativo

Las historias se almacenan en archivos JSON independientes del código del motor.
Este formato equivale al contrato JSON de la guía ("Elemento / Campos y significado").

**Historia** (objeto raíz):

| Campo | Tipo | Significado |
|---|---|---|
| `titulo` | texto | Título de la historia. |
| `inicio` | ID de escena | Escena donde comienza cada partida. |
| `variables` | mapa de booleanos | Valores iniciales del estado de la partida. |
| `escenas` | lista de escenas | Todas las escenas (incluidas las finales). |

**Escena**:

| Campo | Tipo | Significado |
|---|---|---|
| `id` | texto | Identificador único de la escena. |
| `texto` | texto | Contenido visible para el lector. |
| `final` | booleano | Indica si la escena es un desenlace. |
| `opciones` | lista de opciones | Vacía si la escena es final; al menos una si no lo es. |

**Opción**:

| Campo | Tipo | Significado |
|---|---|---|
| `id` | texto | Único dentro de la escena. |
| `texto` | texto | Etiqueta visible en el menú. |
| `destino` | ID de escena | Escena a la que se avanza (debe existir). |
| `condiciones` | mapa de igualdades booleanas | Todas deben cumplirse para habilitar la opción; un mapa vacío la habilita siempre. |
| `efectos` | mapa de asignaciones booleanas | Cambios sobre las variables al elegirla; un mapa vacío conserva las variables. |

Las condiciones y los efectos solo admiten igualdades y asignaciones de
verdadero/falso sobre variables declaradas en `variables`. No hay otras
expresiones.

### Reglas del contenido

1. Los identificadores de las escenas deben ser únicos.
2. La escena inicial debe existir.
3. Los destinos deben corresponder a escenas existentes.
4. Las variables utilizadas en condiciones y efectos deben estar declaradas.
5. Las condiciones y los efectos deben ser booleanos.
6. Las escenas finales deben tener cero opciones y las no finales al menos una.
7. Los archivos deben contener JSON válido y utilizar codificación UTF-8.

El validador (`validar_historia` en `src/main.py`) rechaza la historia antes de
jugar si incumple cualquiera de estas reglas, con un mensaje que indica la causa
y el campo o ID involucrado.

## 8. Rutas para demostrar los finales

Secuencias verificadas ejecutando el motor (cada valor es la tecla/opción que
se elige en cada menú; los números corresponden al orden de las opciones
habilitadas que aparecen en pantalla).

| Demostración | Secuencia en la historia original |
|---|---|
| Final E4 (Rescate) | `1` (Revisar señal) → `1` (Investigar archivo) → `1` (Activar con código) → E4. Salir con `s`. |
| Final E5 (El eco) | `1` (Revisar señal) → `2` (Continuar sin investigar) → `1` (Activar sin verificar) → E5. Salir con `s`. |
| Final E6 (Silencio) | `1` (Revisar señal) → `2` (Continuar sin investigar) → `2` (Cortar comunicación) → E6. Salir con `s`. |
| Efecto de una condición | Sin investigar, en E3 solo aparecen "Activar sin verificar" y "Cortar comunicación"; tras investigar (conoce_origen verdadero) aparece "Activar con código" en su lugar. |
| Ejemplo de deshacer (anexo) | `1` (Revisar) → `1` (Investigar) → en E3, `d` regresa a E2 con conoce_origen falso → `d` se rechaza ("No hay ninguna decisión para deshacer") → `2` (Continuar sin investigar) → E3 muestra "Activar sin verificar" y "Cortar comunicación". |
| Segunda historia | Ejecutar `python src/main.py data/segunda_historia.json`; por ejemplo `1` (Establecer contacto) → `1` (Verificar el código) → `1` (Enviar equipo de rescate) → E4, su final. |

Ejecución reproducible de una ruta (Linux/macOS):

```bash
printf '1\n1\n1\ns\n' | python src/main.py data/historia.json   # termina en E4
```

## 9. Control de versiones

El proyecto utiliza Git para registrar los cambios y GitHub para alojar el repositorio.

Consultar el historial:

```bash
git log --oneline
```

Consultar autores, fechas y mensajes:

```bash
git log --pretty=format:"%h | %an | %ad | %s" --date=short
```

Consultar el estado del repositorio:

```bash
git status
```

El historial permite revisar la evolución del código y recuperar versiones anteriores.

## 10. Limitaciones conocidas

- La interfaz es textual y funciona mediante consola.
- Las historias deben respetar la estructura JSON esperada por el motor.
- La validación detecta únicamente los errores contemplados en el código.
- Los recorridos dependen de las escenas, condiciones, efectos y destinos definidos.
- Las pruebas automatizadas cubren los casos implementados, pero no garantizan la ausencia de todos los errores.
- No se garantiza que el progreso de una partida se conserve entre ejecuciones (no hay guardado).
- El retroceso (deshacer) es de un solo nivel: no existe "rehacer" ni un historial de varios pasos.
- Deshacer solo está disponible cuando hubo una elección válida previa; al iniciar o tras reiniciar no hay retroceso.
- Si en una escena no final ninguna opción queda habilitada, la partida se informa como bloqueada y solo se puede deshacer, reiniciar o salir.
- Los cambios en las reglas o en el formato de los datos pueden requerir actualizar el motor, las historias y las pruebas.

## 11. Bibliotecas y licencias

| Biblioteca o herramienta | Uso | Licencia o condición |
|---|---|---|
| Python | Lenguaje y entorno de ejecución. | PSF License para la distribución habitual de Python. |
| `json` | Lectura de archivos JSON. | Biblioteca estándar de Python. |
| `pathlib` | Gestión de rutas. | Biblioteca estándar de Python. |
| `sys` | Lectura de argumentos. | Biblioteca estándar de Python. |
| `unittest` | Pruebas automatizadas. | Biblioteca estándar de Python. |
| Git | Control de versiones. | GNU GPL v2. |
| GitHub | Alojamiento del repositorio. | Servicio propietario sujeto a sus condiciones de uso. |






# La última transmisión

Motor narrativo interactivo desarrollado en Python. Permite ejecutar historias almacenadas en archivos JSON, tomar decisiones, modificar variables y llegar a diferentes finales.

## 1. Integrantes

- Brayan Maluenga

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
La-Ultima-Transmision/
├── data/
│   ├── Historia.json
│   └── segunda_historia.json
├── docs/
│   ├── RF-06-deshacer.md
│   └── trazabilidad.md
├── src/
│   └── main.py
├── tests/
│   └── test_motor.py
├── .gitignore
└── README.md
```

- `src/main.py`: contiene el motor narrativo.
- `data/Historia.json`: contiene la historia original.
- `data/segunda_historia.json`: contiene una segunda historia.
- `tests/test_motor.py`: contiene las pruebas automatizadas.
- `docs/RF-06-deshacer.md`: documenta el requisito de deshacer.
- `docs/trazabilidad.md`: relaciona los requisitos con la implementación.
- `README.md`: contiene la documentación del proyecto.

## 4. Instalación

### Clonar el repositorio

Reemplaza `URL_DEL_REPOSITORIO` por la URL real de GitHub.

```bash
git clone URL_DEL_REPOSITORIO
cd La-Ultima-Transmision
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
python src/main.py data/Historia.json
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
python -m json.tool data/Historia.json
```

### Validar el formato JSON de la segunda historia

```bash
python -m json.tool data/segunda_historia.json
```

La validación sintáctica de JSON no garantiza que todos los destinos y variables sean correctos. Para ello también se utiliza la validación del motor narrativo.

## 6. Pruebas automatizadas

Ejecuta las pruebas con:

```bash
python -m unittest discover -s tests -v
```

Las pruebas contemplan funcionalidades como:

- Detección de destinos inexistentes.
- Detección de escenas duplicadas.
- Detección de variables no declaradas.
- Restauración del estado anterior al deshacer una decisión.
- Eliminación del historial al reiniciar la partida.
- Comportamiento de deshacer desde un estado final.

Las pruebas deben ejecutarse después de realizar cambios importantes. Los resultados incluidos en la entrega deben corresponder a una ejecución real.

## 7. Formato del contenido narrativo

Las historias se almacenan en archivos JSON independientes del código del motor.

Conceptualmente, cada historia contiene:

- Identificación de la historia.
- Escena inicial.
- Escenas con identificadores únicos.
- Textos narrativos.
- Opciones disponibles.
- Destinos asociados a las opciones.
- Condiciones para habilitar opciones.
- Efectos que modifican variables.
- Escenas finales.

Los nombres exactos de los campos y la estructura de las condiciones y los efectos deben coincidir con los definidos en `src/main.py`.

### Reglas del contenido

1. Los identificadores de las escenas deben ser únicos.
2. La escena inicial debe existir.
3. Los destinos deben corresponder a escenas existentes.
4. Las variables utilizadas deben respetar la estructura del motor.
5. Las condiciones y los efectos deben seguir el formato admitido.
6. Los archivos deben contener JSON válido y utilizar codificación UTF-8.

Se recomienda utilizar las historias existentes como referencia antes de crear una nueva.

## 8. Rutas para demostrar los finales

La historia original debe utilizarse para demostrar sus tres finales y el efecto de las condiciones sobre las opciones disponibles.

| Demostración | Procedimiento |
|---|---|
| Primer final | Ejecutar la historia original y elegir las opciones que conduzcan al primer final. |
| Segundo final | Seguir el recorrido correspondiente al segundo final. |
| Tercer final | Seguir el recorrido correspondiente al tercer final. |
| Efecto de una condición | Modificar una variable mediante una decisión y comprobar cómo afecta una opción posterior. |
| Segunda historia | Ejecutar `python src/main.py data/segunda_historia.json`. |

Las secuencias exactas de decisiones deben completarse después de recorrer `Historia.json` y verificar las rutas reales. No se deben inventar nombres de escenas ni decisiones.

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
- No se garantiza que el progreso de una partida se conserve entre ejecuciones.
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





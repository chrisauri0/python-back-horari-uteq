# python-back-horari-uteq

## Descripción

Este proyecto genera horarios universitarios automáticamente, aplicando restricciones y sugerencias para optimizar la asignación de materias, profesores y aulas.

### Estructura principal

- **main.py**: Microservicio FastAPI. Recibe los datos de materias y grupos vía POST, ejecuta la pipeline de generación y ajuste de horarios, y devuelve el resultado final.
- **horario_greedy.py**: Algoritmo principal de asignación. Genera un horario inicial usando un método greedy, respetando restricciones como horas mínimas de profesores y slots exclusivos para inglés.
- **swap_sugerencias_horario.py**: Genera sugerencias de movimientos y swaps para materias que no pudieron ser asignadas en el horario inicial.
- **aplicar_sugerencias_horario.py**: Aplica las sugerencias generadas, ajustando el horario para intentar asignar todas las materias faltantes.

## Cómo correr el proyecto

1. **Instala dependencias**

   ```bash
   pip install fastapi uvicorn
   ```

2. **Ejecuta el microservicio**

   ```bash
   python main.py
   ```

   Esto inicia el servidor en `http://localhost:8000`.

3. **Envía los datos de materias y grupos**
   Puedes hacer un POST a `/generar-horario` con un JSON como este:

   ```json
   {
     "IDGS14": [
   	 {"id": "Matematicas para ingenieria", "H": 4, "rooms": ["Aula 11 edificio k"], "profs": ["Jesus Hernan"]},
   	 ...
     ],
     "IDGS15": [...],
     "IDGS16": [...]
   }
   ```

   Si no envías datos, se usan datos de prueba.

4. **Pipeline de generación**
   - El microservicio ejecuta:
     1. `horario_greedy.py` para generar el horario inicial.
     2. Si hay materias faltantes, ejecuta `swap_sugerencias_horario.py` y `aplicar_sugerencias_horario.py` para ajustar el horario.
   - El resultado final se devuelve como JSON.

## Explicación de los scripts

### horario_greedy.py

Genera el horario inicial usando un algoritmo greedy. Respeta restricciones como:

- Horas mínimas para profesores (por ejemplo, Angelica solo después de cierta hora).
- Slots exclusivos para inglés por grupo.
- No solapamiento de profesores y aulas.
  Guarda el resultado en `horario_greedy.json` y reporta materias faltantes en `materias_fuera.json`.

### swap_sugerencias_horario.py

Analiza las materias faltantes y genera sugerencias de movimientos (swap/push) para intentar acomodarlas en el horario, sin violar restricciones.
Guarda las sugerencias en `sugerencias_movimientos.json`.

### aplicar_sugerencias_horario.py

Aplica las sugerencias generadas, ajustando el horario y asignando las materias faltantes si es posible.
Guarda el horario final en `horario_greedy_aplicado.json`.

## Notas

- Puedes modificar las restricciones (por ejemplo, hora mínima de Angelica) directamente en el JSON de materias usando el campo `min_hora`.
- El sistema reporta materias faltantes y huecos en los archivos de salida.

## Requisitos

- Python 3.10+ (recomendado)
- FastAPI
- Uvicorn

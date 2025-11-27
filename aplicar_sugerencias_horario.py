# aplicar_sugerencias_horario.py
"""
Aplica automáticamente las sugerencias de movimientos y swaps al horario original,
generando un nuevo archivo de horario ajustado.
"""
import json
import copy
import sys
from pathlib import Path

# --- Configuración de paths ---
if len(sys.argv) > 3:
    horario_path = Path(sys.argv[1])
    sugerencias_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    subjects_path = Path(sys.argv[4]) if len(sys.argv) > 4 else None
else:
    BASE_DIR = Path(__file__).parent.resolve()
    horario_path = BASE_DIR / "horario_greedy.json"
    sugerencias_path = BASE_DIR / "sugerencias_movimientos.json"
    output_path = BASE_DIR / "horario_greedy_aplicado.json"
    subjects_path = None

# --- Cargar archivos ---
with open(horario_path, encoding='utf-8') as f:
    horario = json.load(f)
with open(sugerencias_path, encoding='utf-8') as f:
    sugerencias = json.load(f)

# --- Cargar subjects ---
if subjects_path and subjects_path.exists():
    with open(subjects_path, encoding="utf-8") as f:
        SUBJECTS = json.load(f)
else:
    SUBJECTS = {
        "IDGS14": [
            {"id": "administracion del tiempo", "H": 3, "rooms": ["Aula 12 edificio k"], "profs": ["Maria Guadalupe"]},
            {"id": "Matematicas para ingenieria", "H": 4, "rooms": ["Aula 11 edificio k"], "profs": ["Jesus Hernan"]},
            {"id": "Arquitectura de software", "H": 5, "rooms": ["Aula 11 edificio I"], "profs": ["Manuel"]},
            {"id": "Ingles", "H": 4, "rooms": ["Aula 13 edificio k"], "profs": ["Profe Ingles3"]},
            {"id": "Metodologia de desarrollo de proyectos", "H": 3, "rooms": ["SUMPA edificio k"], "profs": ["Angelica"], "min_hora": 19},
            {"id": "Experiencia de usuario", "H": 3, "rooms": ["Aula 10 edificio j"], "profs": ["Emmanuel"]},
            {"id": "Seguridad informatica", "H": 3, "rooms": ["Aula 12 edificio j"], "profs": ["Brandon"]},
        ],
        "IDGS15": [
            {"id": "administracion del tiempo", "H": 3, "rooms": ["Aula 12 edificio k"], "profs": ["Maria Guadalupe"]},
            {"id": "Matematicas para ingenieria", "H": 4, "rooms": ["Aula 11 edificio k"], "profs": ["Jesus Hernan"]},
            {"id": "Arquitectura de software", "H": 5, "rooms": ["Aula 11 edificio I"], "profs": ["Manuel"]},
            {"id": "Ingles", "H": 4, "rooms": ["Aula 13 edificio k"], "profs": ["Profe Ingles1"]},
            {"id": "Metodologia de desarrollo de proyectos", "H": 3, "rooms": ["SUMPA edificio k"], "profs": ["Angelica"], "min_hora": 19},
            {"id": "Experiencia de usuario", "H": 3, "rooms": ["Aula 10 edificio j"], "profs": ["Emmanuel"]},
            {"id": "Seguridad informatica", "H": 3, "rooms": ["Aula 12 edificio j"], "profs": ["Brandon"]},
        ],
        "IDGS16": [
            {"id": "administracion del tiempo", "H": 3, "rooms": ["Aula 12 edificio k"], "profs": ["Maria Guadalupe"]},
            {"id": "Matematicas para ingenieria", "H": 4, "rooms": ["Aula 11 edificio k"], "profs": ["Jesus Hernan"]},
            {"id": "Arquitectura de software", "H": 5, "rooms": ["Aula 11 edificio I"], "profs": ["Manuel"]},
            {"id": "Ingles", "H": 4, "rooms": ["Aula 13 edificio k"], "profs": ["Profe Ingles2"]},
            {"id": "Metodologia de desarrollo de proyectos", "H": 3, "rooms": ["SUMPA edificio k"], "profs": ["Angelica"], "min_hora": 19},
            {"id": "Experiencia de usuario", "H": 3, "rooms": ["Aula 10 edificio j"], "profs": ["Emmanuel"]},
            {"id": "Seguridad informatica", "H": 3, "rooms": ["Aula 12 edificio j"], "profs": ["Brandon"]},
        ]
    }

# Función para obtener profe y aula
def get_prof_room(materia, grupo):
    for subj in SUBJECTS[grupo]:
        if subj["id"] == materia:
            return subj["profs"][0], subj["rooms"][0]
    return None, None

nuevo_horario = copy.deepcopy(horario)

for sug in sugerencias:
    if sug["accion"] == "asignar_directo":
        grupo = sug["group"]
        materia = sug["materia"]
        slot = sug["slot"]
        prof, room = get_prof_room(materia, grupo)
        nuevo_horario.append({
            "group": grupo,
            "subj": materia,
            "start": slot,
            "room": room,
            "prof": prof
        })
    elif sug["accion"] == "swap":
        grupo = sug["group"]
        materia = sug["materia"]
        slot = sug["slot"]
        prof, room = get_prof_room(materia, grupo)
        # 1. Mover la materia que estaba en ese slot al nuevo slot
        mover = sug["swap"]["mover"]
        for a in nuevo_horario:
            if a["group"] == grupo and a["subj"] == mover["materia"] and a["start"] == mover["from"]:
                a["start"] = mover["to"]
                break
        # 2. Asignar la materia faltante al slot liberado
        nuevo_horario.append({
            "group": grupo,
            "subj": materia,
            "start": slot,
            "room": room,
            "prof": prof
        })
    # Si es sin_solucion, no hacer nada

# Guardar el resultado final
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nuevo_horario, f, ensure_ascii=False, indent=4)

print(f"¡Horario ajustado guardado en {output_path}!")

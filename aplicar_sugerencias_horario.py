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
  "IDGS15": [
    {
      "id": "Matematicas para Ingenieria 1",
      "H": 4,
      "rooms": [
        "Salón 11 Edificio K"
      ],
      "profs": [
        "Jesus Hernan Perez Vazquez"
      ]
    },
    {
      "id": "Ingles",
      "H": 4,
      "rooms": [
        "Salón 13 Edificio K"
      ],
      "profs": [
        "Juan josé Vazquez Rodriguez"
      ]
    },
    {
      "id": "Seguridad Informatica",
      "H": 3,
      "rooms": [
        "Salón 12 Edificio J"
      ],
      "profs": [
        "Brandon Efren Venegas Olvera"
      ]
    },
    {
      "id": "Experiencia de Usuario",
      "H": 3,
      "rooms": [
        "Salon 11 Edificio I",
        "Salon 11 Edificio J"
      ],
      "profs": [
        "Emmanuel Martinez Hernándes"
      ]
    },
    {
      "id": "Arquitectura de software",
      "H": 5,
      "rooms": [
        "Salon 12 Edificio I"
      ],
      "profs": [
        "Manuel Contreras Castillo"
      ]
    },
    {
      "id": "Metodologia de desarrollo deproyectos",
      "H": 3,
      "rooms": [
        "SUMPA Edificio K"
      ],
      "profs": [
        "Angelica Garduño Bustamante"
      ],
      "min_hora": 19
    },
    {
      "id": "Administración del Tiempo",
      "H": 3,
      "rooms": [
        "Salón 12 Edificio K"
      ],
      "profs": [
        "Maria Guadalupe Callejas Ramirez"
      ]
    }
  ],
  "IDGS14": [
    {
      "id": "Matematicas para Ingenieria 1",
      "H": 4,
      "rooms": [
        "Salón 11 Edificio K"
      ],
      "profs": [
        "Jesus Hernan Perez Vazquez"
      ]
    },
    {
      "id": "Ingles",
      "H": 4,
      "rooms": [
        "Salón 13 Edificio K"
      ],
      "profs": [
        "profe ingles 2"
      ]
    },
    {
      "id": "Seguridad Informatica",
      "H": 3,
      "rooms": [
        "Salón 12 Edificio J"
      ],
      "profs": [
        "Brandon Efren Venegas Olvera"
      ]
    },
    {
      "id": "Experiencia de Usuario",
      "H": 3,
      "rooms": [
        "Salon 11 Edificio I",
        "Salon 11 Edificio J"
      ],
      "profs": [
        "Emmanuel Martinez Hernándes"
      ]
    },
    {
      "id": "Arquitectura de software",
      "H": 5,
      "rooms": [
        "Salon 12 Edificio I"
      ],
      "profs": [
        "Manuel Contreras Castillo"
      ]
    },
    {
      "id": "Metodologia de desarrollo deproyectos",
      "H": 3,
      "rooms": [
        "SUMPA Edificio K"
      ],
      "profs": [
        "Angelica Garduño Bustamante"
      ],
      "min_hora": 19
    },
    {
      "id": "Administración del Tiempo",
      "H": 3,
      "rooms": [
        "Salón 12 Edificio K"
      ],
      "profs": [
        "Maria Guadalupe Callejas Ramirez"
      ]
    }
  ],
  "IDGS16": [
    {
      "id": "Matematicas para Ingenieria 1",
      "H": 4,
      "rooms": [
        "Salón 11 Edificio K"
      ],
      "profs": [
        "Jesus Hernan Perez Vazquez"
      ]
    },
    {
      "id": "Ingles",
      "H": 4,
      "rooms": [
        "Salón 13 Edificio K"
      ],
      "profs": [
        "Profe ingles 3"
      ]
    },
    {
      "id": "Seguridad Informatica",
      "H": 3,
      "rooms": [
        "Salón 12 Edificio J"
      ],
      "profs": [
        "Brandon Efren Venegas Olvera"
      ]
    },
    {
      "id": "Experiencia de Usuario",
      "H": 3,
      "rooms": [
        "Salon 11 Edificio I",
        "Salon 11 Edificio J"
      ],
      "profs": [
        "Emmanuel Martinez Hernándes"
      ]
    },
    {
      "id": "Arquitectura de software",
      "H": 5,
      "rooms": [
        "Salon 12 Edificio I"
      ],
      "profs": [
        "Manuel Contreras Castillo"
      ]
    },
    {
      "id": "Metodologia de desarrollo deproyectos",
      "H": 3,
      "rooms": [
        "SUMPA Edificio K"
      ],
      "profs": [
        "Angelica Garduño Bustamante"
      ],
      "min_hora": 19
    },
    {
      "id": "Administración del Tiempo",
      "H": 3,
      "rooms": [
        "Salón 12 Edificio K"
      ],
      "profs": [
        "Maria Guadalupe Callejas Ramirez"
      ]
    }
  ]
}

# Función para obtener profe y aula
def get_prof_room(materia, grupo):
    for subj in SUBJECTS[grupo]:
        if subj["id"] == materia:
            return subj["profs"][0], subj["rooms"][0]
    return None, None

nuevo_horario = copy.deepcopy(horario)
# Función para aplicar swaps en cascada
def aplicar_swap_cascada(asignaciones, swap):
    mover = swap["mover"]
    for a in asignaciones:
        if a["group"] == mover["group"] and a["subj"] == mover["materia"] and a["start"] == mover["from"]:
            a["start"] = mover["to"]
            break
    # Aplicar recursivamente cualquier cascada
    if "cascada" in swap:
        aplicar_swap_cascada(asignaciones, swap["cascada"])

# --- Loop principal sobre sugerencias ---
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
        
        # Aplicar toda la cascada
        aplicar_swap_cascada(nuevo_horario, sug["swap"])
        
        # Asignar la materia faltante al slot liberado
        nuevo_horario.append({
            "group": grupo,
            "subj": materia,
            "start": slot,
            "room": room,
            "prof": prof
        })
    # Si es sin_solucion, no hacer nada

# Guardar el resultado final en la ruta que quieras
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nuevo_horario, f, ensure_ascii=False, indent=4)





print(f"¡Horario ajustado guardado en {output_path}!")

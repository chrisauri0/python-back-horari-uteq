Te hago un ejemplo completo de cómo adaptarlo al inicio:

import json
import random
import sys
from pathlib import Path
import copy

# Datos base
SLOTS_PER_DAY = 5
DAYS = ["Lun", "Mar", "Mie", "Jue", "Vie"]
SLOTS = [f"{d}{17+i}" for d in DAYS for i in range(SLOTS_PER_DAY)]

# Ruta de subjects.json pasada desde main.py
if len(sys.argv) > 1:
    subjects_path = Path(sys.argv[1])
    with open(subjects_path, encoding="utf-8") as f:
        SUBJECTS = json.load(f)
else:
    subjects_path = Path("/tmp/subjects.json")
    SUBJECTS = {
        "IDGS14": [
            {"id": "administracion del tiempo", "H": 3, "rooms": ["Aula 12 edificio k"], "profs": ["Maria Guadalupe"]},
            {"id": "Matematicas para ingenieria", "H": 4, "rooms": ["Aula 11 edificio k"], "profs": ["Jesus Hernan"]},
            {"id": "Arquitectura de software", "H": 5, "rooms": ["Aula 11 edificio I"], "profs": ["Manuel"]},
            {"id": "Ingles", "H": 4, "rooms": ["Aula 13 edificio k"], "profs": ["Profe Ingles3"]},
            {"id": "Metodologia de desarrollo de proyectos", "H": 3, "rooms": ["SUMPA edificio k"], "profs": ["Angelica"]},
            {"id": "Experiencia de usuario", "H": 3, "rooms": ["Aula 10 edificio j"], "profs": ["Emmanuel"]},
            {"id": "Seguridad informatica", "H": 3, "rooms": ["Aula 12 edificio j"], "profs": ["Brandon"]},
        ],
        "IDGS15": [
            {"id": "administracion del tiempo", "H": 3, "rooms": ["Aula 12 edificio k"], "profs": ["Maria Guadalupe"]},
            {"id": "Matematicas para ingenieria", "H": 4, "rooms": ["Aula 11 edificio k"], "profs": ["Jesus Hernan"]},
            {"id": "Arquitectura de software", "H": 5, "rooms": ["Aula 11 edificio I"], "profs": ["Manuel"]},
            {"id": "Ingles", "H": 4, "rooms": ["Aula 13 edificio k"], "profs": ["Profe Ingles1"]},
            {"id": "Metodologia de desarrollo de proyectos", "H": 3, "rooms": ["SUMPA edificio k"], "profs": ["Angelica"]},
            {"id": "Experiencia de usuario", "H": 3, "rooms": ["Aula 10 edificio j"], "profs": ["Emmanuel"]},
            {"id": "Seguridad informatica", "H": 3, "rooms": ["Aula 12 edificio j"], "profs": ["Brandon"]},
        ],
        "IDGS16": [
            {"id": "administracion del tiempo", "H": 3, "rooms": ["Aula 12 edificio k"], "profs": ["Maria Guadalupe"]},
            {"id": "Matematicas para ingenieria", "H": 4, "rooms": ["Aula 11 edificio k"], "profs": ["Jesus Hernan"]},
            {"id": "Arquitectura de software", "H": 5, "rooms": ["Aula 11 edificio I"], "profs": ["Manuel"]},
            {"id": "Ingles", "H": 4, "rooms": ["Aula 13 edificio k"], "profs": ["Profe Ingles2"]},
            {"id": "Metodologia de desarrollo de proyectos", "H": 3, "rooms": ["SUMPA edificio k"], "profs": ["Angelica"]},
            {"id": "Experiencia de usuario", "H": 3, "rooms": ["Aula 10 edificio j"], "profs": ["Emmanuel"]},
            {"id": "Seguridad informatica", "H": 3, "rooms": ["Aula 12 edificio j"], "profs": ["Brandon"]},
        ]
    }

OUTPUT_DIR = subjects_path.parent
horario_greedy_path = OUTPUT_DIR / "horario_greedy.json"
materias_fuera_path = OUTPUT_DIR / "materias_fuera.json"


import copy

def run_greedy():
    grupo_materia_horas = {}
    for g in SUBJECTS:
        for subj in SUBJECTS[g]:
            grupo_materia_horas[(g, subj["id"])] = subj["H"]
    asignaciones = []

    # 1. Asignar inglés a cada grupo en una hora distinta todos los días
    horas_ingles = [17, 18, 19, 20, 21]
    grupos = list(SUBJECTS.keys())
    random.shuffle(horas_ingles)
    horas_por_grupo = {g: horas_ingles[i] for i, g in enumerate(grupos)}
    slots_ingles_por_grupo = {g: set() for g in grupos}
    for g in grupos:
        # Buscar la materia de inglés
        materia_ingles = next((subj for subj in SUBJECTS[g] if subj["id"].lower().startswith("ingles")), None)
        if not materia_ingles:
            continue
        prof = materia_ingles["profs"][0]
        room = materia_ingles["rooms"][0]
        hora = horas_por_grupo[g]
        for dia in DAYS:
            slot = f"{dia}{hora}"
            if grupo_materia_horas[(g, materia_ingles["id"])] > 0:
                asignaciones.append({
                    "group": g,
                    "subj": materia_ingles["id"],
                    "start": slot,
                    "room": room,
                    "prof": prof
                })
                grupo_materia_horas[(g, materia_ingles["id"])] -= 1
                slots_ingles_por_grupo[g].add(slot)

    # 2. Asignar el resto de materias, nunca en los slots ocupados por inglés
    for slot in SLOTS:
        dia = slot[:3]
        grupos_pendientes = list(SUBJECTS.keys())
        random.shuffle(grupos_pendientes)
        profes_slot = set(a["prof"] for a in asignaciones if a["start"] == slot)
        rooms_slot = set(a["room"] for a in asignaciones if a["start"] == slot)
        hora_slot = int(slot[-2:])
        for g in grupos_pendientes:
            # No asignar si el slot está ocupado por inglés para este grupo
            if slot in slots_ingles_por_grupo[g]:
                continue
            materias_disponibles = [subj for subj in SUBJECTS[g] if grupo_materia_horas[(g, subj["id"])] > 0 and not subj["id"].lower().startswith("ingles")]
            opciones = []
            for materia in materias_disponibles:
                prof = materia["profs"][0]
                room = materia["rooms"][0]
                # RESTRICCIÓN: Angelica solo puede dar clase después de la hora mínima
                min_hora = materia.get("min_hora", 19) if prof == "Angelica" else None
                if min_hora is not None and hora_slot < min_hora:
                    continue
                profe_ya_dio = any(a["prof"] == prof and a["group"] == g and a["start"].startswith(dia) for a in asignaciones)
                if profe_ya_dio:
                    continue
                if prof in profes_slot:
                    continue
                if room in rooms_slot:
                    continue
                opciones.append((materia, prof, room))
            if not opciones:
                continue
            materia, prof, room = opciones[0]
            asignaciones.append({
                "group": g,
                "subj": materia["id"],
                "start": slot,
                "room": room,
                "prof": prof
            })
            grupo_materia_horas[(g, materia["id"])] -= 1
            profes_slot.add(prof)
            rooms_slot.add(room)
    # Contar huecos
    total_slots = len(SUBJECTS) * len(SLOTS)
    usados = len(asignaciones)
    huecos = total_slots - usados
    return asignaciones, huecos

# Búsqueda de la mejor solución
best_asignaciones = None
min_huecos = float('inf')
max_intentos = 1000
for intento in range(max_intentos):
    asignaciones, huecos = run_greedy()
    if huecos < min_huecos:
        min_huecos = huecos
        best_asignaciones = copy.deepcopy(asignaciones)
    if min_huecos == 0:
        print(f'Solución perfecta encontrada en el intento {intento+1}!')
        break
else:
    print(f'Mejor solución tiene {min_huecos} huecos tras {max_intentos} intentos.')


with open(horario_greedy_path, "w", encoding="utf-8") as f:
    json.dump(best_asignaciones, f, ensure_ascii=False, indent=4)
print(f"¡Horario generado y guardado en {horario_greedy_path}!")

# Reportar materias que quedaron fuera (horas no asignadas)
def materias_fuera(asignaciones):
    # Inicializar horas restantes por grupo y materia
    horas_restantes = {}
    for g in SUBJECTS:
        for subj in SUBJECTS[g]:
            horas_restantes[(g, subj["id"])] = subj["H"]
    for a in asignaciones:
        horas_restantes[(a["group"], a["subj"])] -= 1
    fuera = []
    for (g, m), h in horas_restantes.items():
        if h > 0:
            fuera.append({"group": g, "materia": m, "horas_faltantes": h})
    return fuera


# Chequeo y reporte detallado de horas asignadas por materia y grupo
fuera = materias_fuera(best_asignaciones)



if fuera:
    print("Materias que quedaron fuera (horas no asignadas):")
    for f in fuera:
        print(f)
    # Guardar en JSON
    with open(materias_fuera_path, "w", encoding="utf-8") as f_json:
        json.dump(fuera, f_json, ensure_ascii=False, indent=4)
    print(f"También guardado en {materias_fuera_path}")
    print("ADVERTENCIA: Hay materias incompletas. Revisa el reporte arriba.")
else:
    print("¡Todas las materias fueron asignadas completamente!")

# Reporte resumen por grupo y materia
print("\nResumen de horas asignadas por grupo y materia:")
asignadas_por_materia = {}
for g in SUBJECTS:
    for subj in SUBJECTS[g]:
        asignadas_por_materia[(g, subj["id"])] = 0
for a in best_asignaciones:
    asignadas_por_materia[(a["group"], a["subj"])] += 1
for g in SUBJECTS:
    print(f"Grupo {g}:")
    for subj in SUBJECTS[g]:
        h_asig = asignadas_por_materia[(g, subj["id"])]
        h_req = subj["H"]
        status = "OK" if h_asig == h_req else f"FALTAN {h_req-h_asig}" if h_asig < h_req else f"SOBRAN {h_asig-h_req}" 
        print(f"  {subj['id']}: asignadas={h_asig}, requeridas={h_req} [{status}]")

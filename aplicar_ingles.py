import json
import sys
from collections import Counter, defaultdict

# Uso: python aplicar_ingles.py horario_greedy.json
if len(sys.argv) < 2:
    print("Uso: python aplicar_ingles.py <horario.json>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = "horario_ingles.json"

with open(input_file, encoding="utf-8") as f:
    horario = json.load(f)

# Agrupar asignaciones de inglés por grupo
ingles_por_grupo = defaultdict(list)
for asignacion in horario:
    if asignacion["subj"].lower().startswith("ingles"):
        ingles_por_grupo[asignacion["group"]].append(asignacion)

# Para cada grupo, encontrar el slot más frecuente de inglés
ingles_slot_preferido = {}
for grupo, asignaciones in ingles_por_grupo.items():
    slots = [a["start"] for a in asignaciones]
    if slots:
        preferido = Counter(slots).most_common(1)[0][0]
        ingles_slot_preferido[grupo] = preferido

# Ajustar asignaciones de inglés para cada grupo
def ajustar_ingles(horario, ingles_slot_preferido):
    nuevo_horario = []
    for asignacion in horario:
        if asignacion["subj"].lower().startswith("ingles"):
            preferido = ingles_slot_preferido.get(asignacion["group"])
            if preferido:
                asignacion["start"] = preferido
        nuevo_horario.append(asignacion)
    return nuevo_horario

horario_ajustado = ajustar_ingles(horario, ingles_slot_preferido)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(horario_ajustado, f, ensure_ascii=False, indent=4)

print(f"Horario ajustado para inglés guardado en {output_file}")

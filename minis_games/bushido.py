#!/usr/bin/python3

"""
Collection organizer and purchase suggester for Bushido
"""

import os
import sys

GAME_NAME = "Bushido"
COMPANY = "GCT"

VALID_FACTIONS = ['Jung Pirates', 'Prefecture of Ryu', 'Savage Wave', 'Ronin', 'Kinshi Temple',
    'The Awoken', 'Cult of Yurei', 'Minimoto Clan', 'Temple of Ro-Kan', 'Shadow Wind Clan',
    'Shiho Clan', 'The Descension', 'Silvermoon Syndicate', 'Ito Clan',]

MY_CURRENT_FACTIONS = ['Jung Pirates', 'Ronin']
MY_FUTURE_FACTIONS = ['Prefecture of Ryu', 'Savage Wave', 'Kinshi Temple', 'Ito Clan',
    'The Awoken', 'Cult of Yurei', 'Minimoto Clan', 'Temple of Ro-Kan', 'Shadow Wind Clan',
    'Shiho Clan', 'The Descension', 'Silvermoon Syndicate']

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('minis_games/DB/BushidoData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/BushidoData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
mini_lines = []
names = set()
for line in lines:
    if line.startswith('#') or line == '':
        continue
    line = line.split('#')[0].strip()
    try:
        model_name, model_faction, model_max, model_own = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if model_name in names:
        print("Duplicate: " + model_name)
    names.add(model_name)
    model_max = int(model_max)
    model_own = int(model_own)
    if model_own > model_max:
        model_own = model_max
    TOTAL_MAX += model_max
    TOTAL_OWN += model_own
    mini_lines.append((model_name, model_faction, model_own, model_max))

# Limiting myself to either the factions I play, or the next faction in the list
faction_map = {}
for item_tuple in mini_lines:
    faction = item_tuple[1]
    if faction not in MY_CURRENT_FACTIONS:
        continue
    if faction not in faction_map:
        faction_map[faction] = [0, 0]
    faction_map[faction][0] += item_tuple[2]
    faction_map[faction][1] += item_tuple[3]
fac_list = []
for map_fac, map_inv in faction_map.items():
    fac_list.append((map_fac, map_inv[0], map_inv[1]))
fac_list = sorted(fac_list, key=lambda x:(x[1]/x[2], x[0]))
FILTERED_FACTION = fac_list[0][0]
if (len(MY_CURRENT_FACTIONS) / len(VALID_FACTIONS)) < (fac_list[0][1] / fac_list[0][2]):
    FILTERED_FACTION = MY_FUTURE_FACTIONS[0]
filtered_list = []
for check_line in mini_lines:
    if FILTERED_FACTION in check_line[1]:
        filtered_list.append(check_line)

item_choice, filtered_list = sort_and_filter(filtered_list, 0)

filtered_list = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("minis_games/output/BushidoOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/BushidoOutput.txt", 'w', encoding="UTF-8")

    double_print("Inventory tracker and purchase suggestions for the Bushido " + \
        "miniatures game.\n", out_file_h)
    own_pct = TOTAL_OWN / TOTAL_MAX * 100
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} models for this game " + \
        f"({own_pct:.2f} percent)", out_file_h)
    double_print(f"Maybe purchase a(n) {item_choice} from {FILTERED_FACTION} (have " + \
        f"{filtered_list[2]} out of {filtered_list[3]})", out_file_h)


#!/usr/bin/python3

"""
Collection organizer and purchase suggester for A Song of Ice and Fire Miniatures Game
"""

import os
import sys

GAME_NAME = "A Song of Ice and Fire"
COMPANY = "CMON"

VALID_FACTIONS = ['Lannister', 'Neutral', 'Stark', 'Free Folk', "Night's Watch", 'Baratheon',
    'Targaryen', 'Greyjoy', 'Martell', 'Bolton']
VALID_TYPES = ['Commander', 'Infantry', 'Cavalry', 'Infantry Attachment', 'Cavalry Attachment',
    'Monster', 'NCU', 'War Machine', 'Cards']

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('minis_games/DB/ASOIAFData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/ASOIAFData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter

def validate_factions(in_factions):
    """
    Validate and cleanup the house/faction information
    """
    ret_list = []
    for in_faction in in_factions.split('/'):
        if in_faction in VALID_FACTIONS:
            ret_list.append(in_faction)
        else:
            print("Unknown faction: " + in_faction)
    return ret_list

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

faction_points = {}
for faction in VALID_FACTIONS:
    faction_points[faction] = 0

TOTAL_MAX = 0
TOTAL_OWN = 0
COMMANDER_COUNT = 0
COMMANDER_OWN = 0
mini_lines = []
names = set()
for line in lines:
    if line.startswith('#') or line == '':
        continue
    line = line.split('#')[0].strip()
    try:
        model_name, model_factions, model_type, model_pts, model_max, model_own = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if model_name in names:
        print("Duplicate: " + model_name)
    names.add(model_name)
    model_factions = validate_factions(model_factions)
    m_types = []
    for m_type in model_type.split('/'):
        if m_type not in VALID_TYPES:
            print("Invalid model type: " + m_type)
        else:
            m_types.append(m_type)
    model_pts = int(model_pts)
    model_max = int(model_max)
    model_own = int(model_own)
    if 'Commander' in m_types:
        COMMANDER_COUNT += 1
        if model_own > 0:
            COMMANDER_OWN += 1
    if model_own > model_max:
        model_own = model_max

    for faction in model_factions:
        faction_points[faction] += model_pts * model_own
    TOTAL_MAX += model_max
    TOTAL_OWN += model_own
    mini_lines.append((model_name, model_factions, m_types, model_pts, model_own, model_max))

faction_choice, filtered_list = sort_and_filter(mini_lines, 1)
type_choice, filtered_list = sort_and_filter(filtered_list, 2)
item_choice, filtered_list = sort_and_filter(filtered_list, 0)

filtered_list = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("minis_games/output/ASOIAFOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/ASOIAFOutput.txt", 'w', encoding="UTF-8")

    double_print("Inventory tracker and purchase suggestions for the Song of Ice and Fire " + \
        "miniatures game.\n", out_file_h)
    own_pct = TOTAL_OWN / TOTAL_MAX * 100
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} list items for this game " + \
        f"({own_pct:.2f} percent)", out_file_h)
    double_print(f"Maybe purchase a(n) {type_choice} from {faction_choice} - perhaps a " + \
        f"{item_choice} (have {filtered_list[4]} out of {filtered_list[5]})", out_file_h)

    double_print(f"\nI own {COMMANDER_OWN} out of {COMMANDER_COUNT} Commanders", out_file_h)

    double_print("\nCurrent points by faction:", out_file_h)
    faction_tuples = sorted(faction_points.items(), key=lambda x:(-1 * x[1], x[0]))
    for faction_item in faction_tuples:
        double_print(f"- {faction_item[0]}: {faction_item[1]}", out_file_h)

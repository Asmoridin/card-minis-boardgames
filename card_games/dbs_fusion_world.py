#!/usr/bin/python3

"""
Collection tracker/management for the DBS Fusion World card game
"""

import os
import sys

GAME_NAME = "Dragon Ball Super Card Game: Fusion World"

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/DBSCGFusionWorld.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/DBSCGFusionWorld.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

sub_type_map = {}
TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
for line in lines:
    line = line.split('#')[0]
    card_name, card_subtypes, card_type, card_color, card_cost, card_number, card_set, \
        card_own = line.split(';')
    card_own = int(card_own)
    if card_subtypes == '':
        print("Missing subtypes:")
        print(line)
        continue
    card_subtypes = card_subtypes.split('/')
    for subtype in card_subtypes:
        if subtype not in sub_type_map:
            sub_type_map[subtype] = 0
        sub_type_map[subtype] += 1
    if card_type not in ['Leader', 'Battle', 'Extra']:
        print("Invalid card type: " + card_type)
        continue
    if card_color not in ['Green', 'Red', 'Blue', 'Yellow']:
        print("Invalid card color: " + card_color)
        continue
    CARD_MAX = 4
    if card_type == 'Leader':
        CARD_MAX = 1
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_subtypes, card_type, card_color, card_cost, card_number, \
        card_set, card_own, CARD_MAX))

# Filter by subtype
chosen_subtype, filtered_list = sort_and_filter(item_list, 1)

#Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 3)

# Filter by card type
chosen_type, filtered_list = sort_and_filter(filtered_list, 2)

# Filter by set
chosen_set, filtered_list = sort_and_filter(filtered_list, 6)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

singleton_traits = []
for subtype in sub_type_map:
    if sub_type_map[subtype] == 1:
        singleton_traits.append(subtype)

print("Folling traits show up only once: " + ', '.join(sorted(singleton_traits)))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/DBSCGFusionWorld.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/DBSCGFusionWorld.txt", 'w', encoding="UTF-8")

    SUMMARY_STRING = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(SUMMARY_STRING, out_file_h)

    sugg_string = f"Buy {picked_item[0] + ' - ' + picked_item[5]} (" + \
        f"{picked_item[3] + ' ' + picked_item[2]}) from {picked_item[6]} (have " + \
        f"{picked_item[7]} out of {picked_item[8]})"
    double_print(sugg_string, out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

#!/usr/bin/python3

"""
Collection tracker and purchase suggestion tool for the Anachronism card game
"""

import os
import sys

GAME_NAME = "Anachronism"

valid_nations = ['Mongol', 'Carthaginian', 'Greek', 'Roman', 'Tribes of Israel', 'Korean',
    'Chinese', 'Japanese', 'Romanian', 'Persian', 'Trojan', 'Germanic', 'Native American',
    'Aztec', 'Egyptian', 'American Frontiersmen', 'Pirate', 'Scottish', 'Briton', 'Maori',
    'Turkish', 'Irish', 'Norse', 'Russian', 'Spanish', 'East Indian', 'Byzantine', 'French',
    'Welsh', 'Italian', 'African Kingdoms', 'Saracen', 'German', 'Holy Roman', 
]

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/AnachronismData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('card_games/DB/AnachronismData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
for line in lines:
    line = line.split('//')[0]
    card_name, in_nation, card_set, card_max, card_own = line.split(';')
    card_own = int(card_own)
    card_max = int(card_max)
    card_nation = []
    for nation in in_nation.split('/'):
        if nation not in valid_nations:
            print("Invalid Nation: " + nation)
        card_nation.append(nation)
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    item_list.append((card_name, card_nation, card_set, card_own, card_max))

nation_map = {}
for item in item_list:
    for nation in item[1]:
        if nation not in nation_map:
            nation_map[nation] = [0, 0]
        nation_map[nation][1] += item[4]
        nation_map[nation][0] += item[3]
nation_sorter = []
for key in nation_map:
    nation_sorter.append((key, nation_map[key][0]/nation_map[key][1], nation_map[key][1] - nation_map[key][0]))
nation_sorter = sorted(nation_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_nation = nation_sorter[0][0]
#print(chosen_nation)

filtered_list = []
set_map = {}
for item in item_list:
    if chosen_nation in item[1]:
        filtered_list.append(item)
        if item[2] not in set_map:
            set_map[item[2]] = [0, 0]
        set_map[item[2]][0] += item[3]
        set_map[item[2]][1] += item[4]
set_sorter = []
for key in set_map:
    set_sorter.append((key, set_map[key][0]/set_map[key][1], set_map[key][1] - set_map[key][0]))
set_sorter = sorted(set_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_set = set_sorter[0][0]
#print(chosen_set)

pick_list = []
for item in filtered_list:
    if item[2] == chosen_set:
        pick_list.append(item)
pick_list = sorted(pick_list, key=lambda x:(x[3]/x[4], -1*(x[3]-x[3]), x[0]))
picked_item = pick_list[0]
#print(picked_item)

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/AnachronismOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/AnachronismOut.txt", 'w', encoding="UTF-8")

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    double_print("Buy %s (%s) from %s (have %d out of %d)" % (picked_item[0], '/'.join(picked_item[1]), picked_item[2], picked_item[3], picked_item[4]), out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")
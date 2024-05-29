#!/usr/bin/python3

"""
Collection tracker/purchase suggester for Dragon Dice
"""

import os
import sys

GAME_NAME = "Dragon Dice"

army_factions = ['Dwarves', 'Coral Elves', 'Goblins', 'Lava Elves', 'Amazons', 'Fire Walkers', \
    'Undead', 'Feral', 'Swamp Stalkers', 'Frostwings', 'Scalders', 'Treefolk', 'Eldarim', \
    'Dracolem']
valid_factions = army_factions + ['Medallion', 'Items', 'Dragons', 'Dragonkin', 'Relics', 'Major Terrain', 'Minor Terrain', 'Special Terrain']

my_current_factions = ['Frostwings', 'Fire Walkers', 'Treefolk', 'Eldarim',]
my_future_factions = ['Amazons', 'Goblins', 'Scalders', 'Undead', 'Feral', 'Swamp Stalkers', 'Dwarves', 'Coral Elves', 'Lava Elves', 'Dracolem']

def getMetaType(in_type):
    if in_type in army_factions:
        return 'Unit'
    elif in_type in ['Special Terrain', 'Major Terrain', 'Minor Terrain']:
        return 'Terrain'
    elif in_type in ['Items', 'Medallion', 'Relics']:
        return 'Item'
    elif in_type in ['Dragons', 'Dragonkin']:
        return 'Dragon'
    else:
        print("Unhandled meta type: " + in_type)
        return('Unhandled')

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/DragonDiceCollection.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/DragonDiceCollection.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
faction_total = {}
for line in lines:
    dice_name, dice_faction, dice_size, own = line.split(';')
    if dice_faction not in valid_factions:
        print("Invalid faction: " + dice_faction)
    own = int(own)
    dice_max = 1
    if dice_faction not in faction_total:
        faction_total[dice_faction] = 0
    if dice_size == "Rare":
        if dice_faction in ['Items', 'Dragonkin']:
            dice_max = max(own, 1)
        else:
            dice_max = max(own, 2)
        faction_total[dice_faction] += (own * 3)
    elif dice_size == "Uncommon":
        if dice_faction in ['Items', 'Dragonkin']:
            dice_max = max(own, 2)
        else:
            dice_max = max(own, 4)
        faction_total[dice_faction] += (own * 2)
    elif dice_size == "Common":
        if dice_faction in ['Items', 'Dragonkin']:
            dice_max = max(own, 4)
        else:
            dice_max = max(own, 8)
        faction_total[dice_faction] += (own)
    elif dice_size == "Monster" or dice_size == "Champion" or dice_size == "Artifact" or dice_size == "Dragon":
        dice_max = max(own, 1)
        faction_total[dice_faction] += (own * 4)
    elif dice_faction == "Major Terrain":
        dice_max = max(own, 2)
    elif dice_faction in ['Minor Terrain', 'Special Terrain']:
        dice_max = max(own, 1)
    else:
        print("Unhandled dice size: " + dice_size)
    TOTAL_MAX += dice_max
    TOTAL_OWN += own
    item_list.append((dice_name, dice_faction, dice_size, own, dice_max))

meta_map = {}
for item in item_list:
    if getMetaType(item[1]) not in meta_map:
        meta_map[getMetaType(item[1])] = [0, 0]
    meta_map[getMetaType(item[1])][1] += item[4]
    meta_map[getMetaType(item[1])][0] += item[3]
meta_sorter = []
for key in meta_map:
    meta_sorter.append((key, meta_map[key][0]/meta_map[key][1], meta_map[key][1] - meta_map[key][0]))
meta_sorter = sorted(meta_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_meta = meta_sorter[0][0]
#print(meta_sorter)

faction_map = {}
for item in item_list:
    if getMetaType(item[1]) != chosen_meta:
        continue
    if chosen_meta == 'Unit' and item[1] not in my_current_factions:
        continue
    if item[1] not in faction_map:
        faction_map[item[1]] = [0, 0]
    faction_map[item[1]][1] += item[4]
    faction_map[item[1]][0] += item[3]
faction_sorter = []
for key in faction_map:
    faction_sorter.append((key, faction_map[key][0]/faction_map[key][1], faction_map[key][1] - faction_map[key][0]))
faction_sorter = sorted(faction_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_faction = faction_sorter[0][0]
#chosen_faction="Frostwings"

filtered_list = []
size_map = {}
for item in item_list:
    if item[1] == chosen_faction:
        filtered_list.append(item)
        if item[2] not in size_map:
            size_map[item[2]] = [0, 0]
        size_map[item[2]][0] += item[3]
        size_map[item[2]][1] += item[4]
size_sorter = []
for key in size_map:
    size_sorter.append((key, size_map[key][0]/size_map[key][1], size_map[key][1] - size_map[key][0]))
size_sorter = sorted(size_sorter, key=lambda x:(x[1], -x[2], x[0]))
#print(size_sorter)
chosen_size = size_sorter[0][0]

pick_list = []
for item in filtered_list:
    if item[2] == chosen_size:
        pick_list.append(item)
pick_list = sorted(pick_list, key=lambda x:(x[3]/x[4], -1*(x[4]-x[3]), x[0]))
picked_item = pick_list[0]

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/DragonDiceOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/DragonDiceOut.txt", 'w', encoding="UTF-8")

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    next_buy_string = "Buy a %s from %s - perhaps a %s (have %d out of %d %s)" % (picked_item[2], picked_item[1], picked_item[0], faction_map[picked_item[1]][0], faction_map[picked_item[1]][1], picked_item[1])
    double_print(next_buy_string, out_file_h)

    double_print("Summary:", out_file_h)
    for faction in sorted(army_factions):
        double_print("%s: %d" % (faction, faction_total[faction]), out_file_h)

    out_file_h.close()
    
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

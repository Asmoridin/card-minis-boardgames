#!/usr/bin/python3

"""
Collection tracker and purchase suggestion tool for the City of Heroes card game
"""

import os
import sys

GAME_NAME = "City of Heroes"

def validateType(in_type):
    """
    Standardize the card types
    """
    if in_type in ['Power'] or 'Sig Power' in in_type or in_type.startswith('Power •'):
        return "Power"
    if in_type in ['Mission'] or in_type.startswith('Mission'):
        return "Mission"
    if in_type in ['Enhancement', 'Edge']:
        return in_type
    if in_type.startswith('Sidekick'):
        return 'Sidekick'
    if in_type.startswith('Hero'):
        return 'Hero'
    print("Invalid type: " + in_type)
    return None

def validatePowers(in_power):
    """
    Standard the card powers
    """
    valid_powers = ['War Mace', 'Trick Arrow', 'Super Strength', 'Super Reflexes',
        'Storm Summoning', 'Stone Melee', 'Stone Armor', 'Spines', 'Sonic Resonance',
        'Sonic Attack', 'Regeneration', 'Radiation Emission', 'Radiation Blast', 'Psychic Blast',
        'Mind Control', 'Martial Arts', 'Kinetics', 'Katana', 'Invulnerability',
        'Illusion Control', 'Ice Melee', 'Ice Manipulation', 'Ice Control', 'Ice Blast',
        'Ice Armor', 'Gravity Control', 'Force Field', 'Fire Manipulation', 'Fire Control',
        'Fire Blast', 'Fiery Melee', 'Fiery Aura', 'Energy Melee', 'Energy Manipulation',
        'Energy Blast', 'Empathy', 'Electrical Manipulation', 'Electrical Blast',
        'Earth Control', 'Devices', 'Dark Miasma', 'Dark Melee', 'Dark Blast', 'Dark Armor',
        'Common Pool', 'Claws', 'Broad Sword', 'Battle Axe', 'Assault Rifle', 'Archery'
    ]
    if in_power in valid_powers:
        return in_power
    if in_power.replace(' 1', '') in valid_powers:
        return in_power.replace(' 1', '')
    if in_power.replace(' 2', '') in valid_powers:
        return in_power.replace(' 2', '')
    if in_power.replace(' 3', '') in valid_powers:
        return in_power.replace(' 3', '')
    if in_power.replace(' 4', '') in valid_powers:
        return in_power.replace(' 4', '')
    if in_power.replace(' 6', '') in valid_powers:
        return in_power.replace(' 6', '')
    print("Invalid Power: " + in_power)
    return None

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/CityOfHeroesData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('card_games/DB/CityOfHeroesData.txt', 'r', encoding="UTF-8")
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
    card_name, card_type, card_powers, card_rarity, card_set, card_own = line.split(';')
    card_type = validateType(card_type)
    if card_type == "Power":
        card_powers = validatePowers(card_powers)
    else:
        card_powers = None
    card_own = int(card_own)
    if card_type == 'Hero':
        card_max = 1
    else:
        card_max = 3
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    item_list.append((card_name, card_type, card_powers, card_rarity, card_set, card_own, card_max))

# Filter by set
set_map = {}
for item in item_list:
    if item[4] not in set_map:
        set_map[item[4]] = [0, 0]
    set_map[item[4]][1] += item[6]
    set_map[item[4]][0] += item[5]
set_sorter = []
for key in set_map:
    set_sorter.append((key, set_map[key][0]/set_map[key][1], set_map[key][1] - set_map[key][0]))
set_sorter = sorted(set_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_set = set_sorter[0][0]
#print(chosen_set)

# Filter by card type
filtered_list = []
type_map = {}
for item in item_list:
    if chosen_set == item[4]:
        filtered_list.append(item)
        if item[1] not in type_map:
            type_map[item[1]] = [0, 0]
        type_map[item[1]][0] += item[5]
        type_map[item[1]][1] += item[6]
type_sorter = []
for key in type_map:
    type_sorter.append((key, type_map[key][0]/type_map[key][1], type_map[key][1] - type_map[key][0]))
type_sorter = sorted(type_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_type = type_sorter[0][0]
#print(chosen_type)

pick_list = []
for item in filtered_list:
    if item[1] == chosen_type:
        pick_list.append(item)
pick_list = sorted(pick_list, key=lambda x:(x[5]/x[6], -1*(x[5]-x[5]), x[0]))
picked_item = pick_list[0]
#print(picked_item)

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/CityOfHeroesOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/CityOfHeroesOut.txt", 'w', encoding="UTF-8")

    double_print("Have %d out of %d - %.2f percent" % (TOTAL_OWN, TOTAL_MAX, 100*TOTAL_OWN/TOTAL_MAX), out_file_h)
    double_print("Buy %s (%s) from %s (have %d out of %d)" % (picked_item[0], picked_item[1], picked_item[4], picked_item[5], picked_item[6]), out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")
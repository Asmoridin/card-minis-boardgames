#!/usr/bin/python3

"""
Collection tracker/purchase recommender for the Star Wars Unlimited card game.
"""

import os
import sys

GAME_NAME = "Star Wars: Unlimited"

valid_types = ['Leader', 'Base', 'Ground Unit', 'Space Unit', 'Event', 'Upgrade']
card_rarities = {'C':'Common', 'U':'Uncommon', 'R': 'Rare', 'S':'Special', 'L':'Legendary'}
card_colors_map = {'U':'Blue', 'B':'Black', 'R':'Red', 'G':'Green', 'W':'White', 'Y':'Yellow', }

def process_card_set(card_set_in):
    """
    Given a string of card set information, process it into tuples, and return them.
    """
    ret_list = []
    for card_printing in card_set_in.split('/'):
        card_set, card_number, card_rarity = card_printing.split('-')
        if card_set == 'SOR':
            card_set = 'Spark of Rebellion'
        else:
            print(f"Unknown card set {card_set}")
            return []

        if card_rarity in card_rarities:
            card_rarity = card_rarities[card_rarity]
        else:
            print(f"Unknown card rarity {card_rarity}")
            return []

        ret_list.append((card_set, card_number, card_rarity))
    return ret_list

def convert_colors(in_color):
    """
    Takes in a string, and then returns a list of card colors for this card
    """
    ret_list = []
    for color in in_color.split('/'):
        if color in card_colors_map:
            ret_list.append(card_colors_map[color])
        else:
            print(f"Unknown color {color}")
            return []
    return ret_list

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
for line in lines:
    if line == '':
        continue
    line = line.split('#')[0].strip() # Clears comments on lines
    try:
        card_name, card_set_info, card_type, card_colors, card_owned = line.split(';')
    except ValueError:
        print("Following line isn't formatted correctly:")
        print(line)
        continue
    card_set_tuples = process_card_set(card_set_info)
    if not card_set_tuples:
        continue

    if card_type not in valid_types:
        print(f"Invalid card type {card_type}")
        continue
    card_colors = convert_colors(card_colors)
    if not card_colors:
        continue

    card_owned = int(card_owned)
    CARD_MAX = 3
    if card_type in ['Leader', 'Base']:
        CARD_MAX = 1
    if card_owned > CARD_MAX:
        CARD_MAX = card_owned

    TOTAL_MAX += CARD_MAX
    TOTAL_OWN += card_owned
    item_list.append((card_name, card_set_tuples, card_type, card_colors, card_owned, CARD_MAX))

# Figure out set I'm missing the most.
set_map = {}
for card in item_list:
    for card_set in card[1]:
        if card_set[0] not in set_map:
            set_map[card_set[0]]  = [0, 0]
        set_map[card_set[0]][1] += card[5]
        set_map[card_set[0]][0] += card[4]
set_sorter = []
for key in set_map:
    set_sorter.append((key, set_map[key][0]/set_map[key][1], set_map[key][1] - set_map[key][0]))
set_sorter = sorted(set_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_set = set_sorter[0][0]

# Figure out color I'm missing the most
filtered_list = []
color_map = {}
for card in item_list:
    VALID = False
    for card_set in card[1]:
        if card_set[0] == chosen_set:
            VALID = True
    if not VALID:
        continue
    filtered_list.append(card)
    for color in card[3]:
        if color not in color_map:
            color_map[color]  = [0, 0]
        color_map[color][1] += card[5]
        color_map[color][0] += card[4]
color_sorter = []
for key in color_map:
    color_sorter.append((key, color_map[key][0]/color_map[key][1], color_map[key][1] - color_map[key][0]))
color_sorter = sorted(color_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_color = color_sorter[0][0]
item_list = filtered_list

# Figure out type I'm missing the most
type_map = {}
filtered_list = []
for card in item_list:
    if chosen_color not in card[3]:
        continue
    filtered_list.append(card)
    if card[2] not in type_map:
        type_map[card[2]] = [0, 0]
    type_map[card[2]][1] += card[5]
    type_map[card[2]][0] += card[4]
type_sorter = []
for key in type_map:
    type_sorter.append((key, type_map[key][0]/type_map[key][1], type_map[key][1] - type_map[key][0]))
type_sorter = sorted(type_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_type = type_sorter[0][0]
item_list = filtered_list

# Finally, figure out rarity I'm missing the most
rarity_map = {}
filtered_list = []
for card in item_list:
    if card[2] != chosen_type:
        continue
    filtered_list.append(card)
    for set_info in card[1]:
        if set_info[0] != chosen_set:
            continue
        if set_info[2] not in rarity_map:
            rarity_map[set_info[2]] = [0, 0]
        rarity_map[set_info[2]][1] += card[5]
        rarity_map[set_info[2]][0] += card[4]
rarity_sorter = []
for key in rarity_map:
    rarity_sorter.append((key, rarity_map[key][0]/rarity_map[key][1], rarity_map[key][1] - rarity_map[key][0]))
rarity_sorter = sorted(rarity_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_rarity = rarity_sorter[0][0]

pick_list = []
for item in filtered_list:
    for set_info in item[1]:
        if set_info[0] == chosen_set and set_info[2] == chosen_rarity:
            pick_list.append(item)
pick_list = sorted(pick_list, key=lambda x:(x[4]/x[5], -1*(x[5]-x[4]), x[0]))
picked_item = pick_list[0]

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/StarWarsUnlimited.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/StarWarsUnlimited.txt", 'w', encoding="UTF-8")

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    next_buy_string = f"Buy a {chosen_color} {chosen_type} from {chosen_set} - perhaps {picked_item[0]} (have {picked_item[4]} out of {picked_item[5]})"
    double_print(next_buy_string, out_file_h)

    out_file_h.close()
    
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

#!/usr/bin/python3

"""
Collection manager/purchase suggester for Lorcana
"""

import os
import sys

GAME_NAME = "Lorcana"

valid_types = ['Character', 'Action', 'Item', 'Location', ]
valid_colors = ['Emerald', 'Ruby', 'Sapphire', 'Steel', 'Amber', 'Amethyst', ]


if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/LorcanaData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/LorcanaData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
card_names = set()
item_list = []
for line in lines:
    line = line.split('#')[0].strip()
    card_name, card_type, card_color, card_set, card_rarity, card_own = line.split(';')
    if card_name in card_names:
        print("Duplicate card name: " + card_name)
    card_names.add(card_name)
    if card_type not in valid_types:
        print("Invalid card type: " + card_type)
    if card_color not in valid_colors:
        print("Invalid card color: " + card_color)
    if card_rarity not in ['Common', 'Uncommon', 'Rare', 'Super Rare', 'Legendary']:
        print("Invalid rarity: " + card_rarity)
    card_own = int(card_own)

    CARD_MAX = 4
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_type, card_color, card_set, card_rarity, card_own, CARD_MAX))

# Filter by card_set
chosen_set, filtered_list = sort_and_filter(item_list, 3)

#Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 2)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 1)

# Filter by rarity
chosen_rarity, filtered_list = sort_and_filter(filtered_list, 4)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/LorcanaOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/LorcanaOut.txt", 'w', encoding="UTF-8")

    double_print("Have %d out of %d - %.2f percent" % (TOTAL_OWN, TOTAL_MAX, 100*TOTAL_OWN/TOTAL_MAX), out_file_h)
    double_print("Buy %s (%s) from %s (have %d out of %d)" % (picked_item[0], ' '.join([chosen_rarity, chosen_color, chosen_type]), picked_item[3], picked_item[5], picked_item[6]), out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

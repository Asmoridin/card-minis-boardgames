#!/usr/bin/python3

"""
Collection tracker/purchase recommender for the Star Wars Unlimited card game.
"""

import os
import sys

GAME_NAME = "Star Wars: Unlimited"

valid_types = ['Leader', 'Base', 'Ground Unit', 'Space Unit', 'Event', 'Upgrade']
card_rarities = {'C':'Common', 'U':'Uncommon', 'R': 'Rare', 'S':'Special', 'L':'Legendary'}
card_colors_map = {'U':'Blue', 'B':'Black', 'R':'Red', 'G':'Green',
                   'W':'White', 'Y':'Yellow', 'N':'Neutral'}

def process_card_set(card_set_in):
    """
    Given a string of card set information, process it into list, and return them.
    """
    ret_list = []
    ret_card_sets = []
    ret_card_rarities = []
    for card_printing in card_set_in.split('/'):
        check_card_set, _, card_rarity = card_printing.split('-')
        if check_card_set == 'SOR':
            check_card_set = 'Spark of Rebellion'
        elif check_card_set == 'SHD':
            check_card_set = 'Shadows of the Galaxy'
        else:
            print(f"Unknown card set {check_card_set}")
            return []

        if card_rarity in card_rarities:
            card_rarity = card_rarities[card_rarity]
        else:
            print(f"Unknown card rarity {card_rarity}")
            return []

        ret_card_sets.append(check_card_set)
        ret_card_rarities.append(card_rarity)
    ret_list = [ret_card_sets, ret_card_rarities]
    return ret_list

def convert_colors(in_color):
    """
    Takes in a string, and then returns a list of card colors for this card
    """
    ret_list = []
    for color_code in in_color.split('/'):
        if color_code in card_colors_map:
            ret_list.append(card_colors_map[color_code])
        else:
            print(f"Unknown color {color_code}")
            return []
    return ret_list

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
for line in lines:
    if line == '' or line.startswith('#'):
        continue
    line = line.split('#')[0].strip() # Clears comments on lines
    try:
        card_name, card_set_info, card_type, card_colors, card_owned = line.split(';')
    except ValueError:
        print("Following line isn't formatted correctly:")
        print(line)
        continue
    this_card_sets, this_card_rarities = process_card_set(card_set_info) # pylint: disable=unbalanced-tuple-unpacking

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
    item_list.append((card_name, this_card_sets, this_card_rarities, card_type, card_colors,
        card_owned, CARD_MAX))

# Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 1)

# Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 4)

# Filter by card type
chosen_type, filtered_list = sort_and_filter(filtered_list, 3)

# Filter by rarity
chosen_rarity, filtered_list = sort_and_filter(filtered_list, 2)

# Pick a card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/StarWarsUnlimited.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/StarWarsUnlimited.txt", 'w', encoding="UTF-8")

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    next_buy_string = f"Buy a {chosen_color} {chosen_type} from {chosen_set} - perhaps " + \
        f"{picked_item[0]} (have {picked_item[5]} out of {picked_item[6]})"
    double_print(next_buy_string, out_file_h)
    out_file_h.close()

    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

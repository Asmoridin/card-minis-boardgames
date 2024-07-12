#!/usr/bin/python3

"""
Collection tracker/management for the One Piece card game
"""

import os
import sys

GAME_NAME = "One Piece"

def validate_colors(in_colors):
    """
    Takes in a string of colors, and returns a list with the full color names
    """
    ret_colors = []
    color_map = {'U':'Blue', 'G':'Green', 'R':'Red', 'P':'Purple', 'B':'Black', 'Y':'Yellow'}
    for color in in_colors.split('/'):
        if color not in color_map:
            print("Invalid color: " + color)
        else:
            ret_colors.append(color_map[color])
    return ret_colors

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/OnePieceData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/OnePieceData.txt', 'r', encoding="UTF-8")
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
dupe_check = set()
num_leaders = 0
for line in lines:
    line = line.split('#')[0]
    try:
        card_name, card_number, card_type, card_color, card_subtypes, card_set, \
            card_own = line.split(';')
    except ValueError:
        print("Possibly invalid line:")
        print(line)
        continue
    if (card_name, card_number) in dupe_check:
        print("Possible duplicate: ")
        print(line)
    dupe_check.add((card_name, card_number))
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
    if card_type not in ['Leader', 'Character', 'Event', 'Stage']:
        print("Invalid card type: " + card_type)
        continue
    card_color = validate_colors(card_color)
    card_set = card_set.split('/')
    CARD_MAX = 4
    if card_type == 'Leader':
        CARD_MAX = 1
        num_leaders += 1
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_number, card_type, card_color, card_subtypes, card_set, \
        card_own, CARD_MAX))

# Filter by subtype
chosen_subtype, filtered_list = sort_and_filter(item_list, 4)

# If there's an available Leader, let's make sure we filter to them.
HAS_LEADER = False
leader_list = []
for card_tuple in filtered_list:
    if card_tuple[2] == 'Leader' and card_tuple[6] == 0:
        HAS_LEADER = True
        leader_list.append(card_tuple)
if HAS_LEADER:
    filtered_list = leader_list

#Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 3)

# Filter by card type
chosen_type, filtered_list = sort_and_filter(filtered_list, 2)

# Filter by set
chosen_set, filtered_list = sort_and_filter(filtered_list, 5)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

singleton_traits = []
for subtype, subtype_count in sub_type_map.items():
    if subtype_count == 1:
        singleton_traits.append(subtype)

print("Following traits show up only once: " + ', '.join(sorted(singleton_traits)))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/OnePieceOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/OnePieceOut.txt", 'w', encoding="UTF-8")

    SUMMARY_STRING = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(SUMMARY_STRING, out_file_h)

    double_print(f"\nThere are {num_leaders} leaders in the game\n", out_file_h)

    double_print(f"Chosen subtype is {chosen_subtype}, chosen color is {chosen_color}", out_file_h)
    double_print(f"Chosen card type: {chosen_type}, and chosen set: {chosen_set}", out_file_h)
    sugg_string = f"Buy {picked_item[0]} (have " + \
        f"{picked_item[6]} out of {picked_item[7]})"
    double_print(sugg_string, out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

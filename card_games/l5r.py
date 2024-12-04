#!/usr/bin/python3

"""
Inventory tracker and purchase selector for the Legend of the Five Rings CCG
"""

import os
import re
import sys

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/L5RData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('card_games/DB/L5RData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter

DYNASTY_CARD_TYPES = ['Region', 'Event', 'Holding']
FATE_CARD_TYPES = ['Strategy', 'Spell', 'Item']
PREGAME_TYPES = ['Stronghold']

VALID_CLANS = ['Lion', 'Shadowlands']

MODERN_SETS = ['Ivory Edition', 'The Dead of Winter', 'Emperor Edition Demo Decks',
    'Death at Koten', 'Promotional-Celestial', 'Promotional-Samurai', 'Before the Dawn',
    'Battle of Kyuden Tonbo', 'The Harbinger', 'Emperor Edition', 'Forgotten Legacy',
    'Second City', 'Promotional-Ivory', 'Glory of the Empire', 'Stronger Than Steel',
    'Celestial Edition', 'The Truest Test', 'Twenty Festivals', 'The Imperial Gift 3',
    'Samurai Edition', 'Tomorrow', "Khan's Defiance", "Promotional-Twenty Festivals",
    "The Plague War", 'The Currency of War', 'Samurai Edition Banzai', 'War of Honor',
    'The Imperial Gift 2',
]
PRE_MODERN_SETS = ['Hidden Emperor 6', 'Diamond Edition', 'Training Grounds', 'Winds of Change',
    'Hidden Emperor 4', "Honor's Veil", 'The Dark Journey Home', '1,000 Years of Darkness',
    'The Fall of Otosan Uchi', 'Forbidden Knowledge', 'Lotus Edition', "Ambition's Debt",
    'Test of Enlightenment', 'A Perfect Cut', 'Rise of the Shogun', 'Scorpion Clan Coup 3',
    'Promotional-Lotus', 'Training Grounds 2', 'Hidden City', 'Heaven & Earth', 'Shadowlands',
    'Gold Edition', 'Jade Edition', 'Pearl Edition', 'Crimson and Jade', 'Time of the Void',
    'Path of Hope', 'Anvil of Despair', "An Oni's Fury", 'Honor Bound', 'Promotional-Gold',
    'Promotional-Diamond', 'Scorpion Clan Coup 1', 'The War of Spirits', 'Dark Allies',
    'Promotional-Imperial', 'Soul of the Empire', 'Promotional-Jade',
]
VALID_FORMATS = ['Race for the Throne (Samurai)', 'Age of Enlightenment (Lotus)',
    'Hidden Emperor (Jade)', 'Destroyer War (Celestial)', 'Four Winds (Gold)', 'Modern',
    "A Brother's Destiny (Twenty Festivals)", "A Brother's Destiny (Ivory Edition)",
    'Age of Conquest (Emperor)', 'Clan Wars (Imperial)', 'Rain of Blood (Diamond)',
    'Onyx Edition']

def parse_sets(this_card_name, set_string):
    """
    Take in a set string, and return a tuple:
    ([sets], [rarites], MODERN_LEGAL (bool))
    """
    set_string = set_string.replace('–', '-')
    ret_sets = []
    ret_rarities = set()
    ret_modern_legal = False
    for set_part in set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", set_part)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            if this_set in MODERN_SETS:
                ret_modern_legal = True
            elif this_set in PRE_MODERN_SETS:
                pass
            else:
                print(f"Unhandled set for modern check: {this_set}")
            ret_sets.append(this_set)
            ret_rarities.add(this_set_rarity)
        else:
            print("[" + this_card_name + "] Issue with: " + set_part)
    return (ret_sets, list(ret_rarities), ret_modern_legal)

in_lines = file_h.readlines()
file_h.close()
in_lines = [line.strip() for line in in_lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
card_lines = []
modern_cards = {} # A dictionary of names -> card lines for Modern legal cards
format_map = {} # For a format summary at the end, given that this is our first criteria
for set_format in VALID_FORMATS:
    format_map[set_format] = [0, 0]
for line in in_lines:
    if line.startswith('#') or line == '':
        continue
    try:
        card_name, card_type, card_clan, card_sets, card_format, card_max, \
            card_own = line.split(';')
    except ValueError:
        print("Invalid line:")
        print(line)
        continue
    CARD_DECK = ''
    if card_type in DYNASTY_CARD_TYPES:
        CARD_DECK = 'Dynasty'
    elif card_type in FATE_CARD_TYPES:
        CARD_DECK = 'Fate'
    elif card_type in PREGAME_TYPES:
        CARD_DECK = 'Pre-Game'
    else:
        print(f"Unknown card type: {card_type}")
        continue
    if card_clan != '' and card_clan not in VALID_CLANS:
        print(f"Invalid clan: {card_clan}")
        continue
    card_sets, card_rarities, modern_legal = parse_sets(card_name, card_sets)
    if card_format not in VALID_FORMATS:
        print(f"Invalid format: {card_format}")
        continue
    card_max = int(card_max)
    card_own = int(card_own)
    format_map[card_format][0] += card_own
    format_map[card_format][1] += card_max
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    if modern_legal:
        if card_name not in modern_cards:
            modern_cards[card_name] = [card_name, card_type, CARD_DECK, card_clan, card_sets, \
                card_rarities, 'Modern', min(card_own, 1), 1]
        else:
            modern_cards[card_name][4] = list(set(modern_cards[card_name][4] + card_sets))
            modern_cards[card_name][5] = list(set(modern_cards[card_name][5] + card_rarities))
            modern_cards[card_name][7] = min(modern_cards[card_name][8], \
                modern_cards[card_name][7] + card_own)

    card_lines.append([card_name, card_type, CARD_DECK, card_clan, card_sets, card_rarities, \
        card_format, card_own, card_max])

for _, card_item in modern_cards.items():
    card_lines.append(card_item)
    format_map['Modern'][0] += card_item[7]
    format_map['Modern'][1] += card_item[8]

format_choice, filtered_list = sort_and_filter(card_lines, 6)
deck_choice, filtered_list = sort_and_filter(filtered_list, 2)
set_choice, filtered_list = sort_and_filter(filtered_list, 4)
type_choice, filtered_list = sort_and_filter(filtered_list, 1)
CLAN_CHOICE = ""
if type_choice in ['Personality', 'Stronghold']:
    CLAN_CHOICE, filtered_list = sort_and_filter(filtered_list, 3)
_, filtered_list = sort_and_filter(filtered_list, 5)
card_name, filtered_list = sort_and_filter(filtered_list, 0)

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/L5ROut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/L5ROut.txt", 'w', encoding="UTF-8")

    double_print("Legend of the Five Rings CCG Inventory Tracker Tool\n", out_file_h)
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} total cards - " + \
        f"{100 * TOTAL_OWN/TOTAL_MAX:.2f} percent\n", out_file_h)

    if CLAN_CHOICE == "":
        type_str = type_choice
    else:
        type_str = CLAN_CHOICE + " " + type_choice
    double_print(f"Suggested purchase is a {type_str} from {set_choice}: {card_name} (own " + \
        f"{filtered_list[0][7]} out of {filtered_list[0][8]})", out_file_h)

    double_print("\nCurrent inventory percentage by format:", out_file_h)
    format_sorter = format_map.items()
    format_sorter = sorted(format_sorter, key=lambda x:(-1 * x[1][0]/x[1][1], x[1][1] - x[1][0]))
    for format_name, fown in format_sorter:
        double_print(f"{format_name}: {100*fown[0]/fown[1]:.2f} ({fown[0]}/{fown[1]})", out_file_h)

    out_file_h.close()

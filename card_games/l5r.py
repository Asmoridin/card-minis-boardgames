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

DYNASTY_CARD_TYPES = ['Region', 'Event']
FATE_CARD_TYPES = ['Strategy']
MODERN_SETS = ['Ivory Edition']
PRE_MODERN_SETS = ['Hidden Emperor 6']


def parse_sets(this_card_name, set_string):
    """
    Take in a set string, and return a tuple:
    ([sets], [rarites], MODERN_LEGAL (bool))
    """
    ret_sets = []
    ret_rarities = set()
    modern_legal = False
    for set_part in set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", set_part)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            if this_set in MODERN_SETS:
                modern_legal = True
            elif this_set in PRE_MODERN_SETS:
                pass
            else:
                print(f"Unhandled set for modern check: {this_set}")
            ret_rarities.add(this_set_rarity)
        else:
            print("[" + this_card_name + "] Issue with: " + set_part)
    return (ret_sets, list(ret_rarities), modern_legal)

in_lines = file_h.readlines()
file_h.close()
in_lines = [line.strip() for line in in_lines]

card_lines = []
for line in in_lines:
    if line.startswith('#') or line == '':
        continue
    try:
        card_name, card_type, card_clan, card_sets, card_formats, card_max, \
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
    else:
        print(f"Unknown card type: {card_type}")
        continue
    if card_clan != '':
        print(card_clan)
    print(parse_sets(card_name, card_sets))
    card_lines.append([card_name, card_type, CARD_DECK, card_clan, card_sets, card_formats, \
        card_max, card_own])

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/L5ROut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/L5ROut.txt", 'w', encoding="UTF-8")

    double_print("Legend of the Five Rings CCG Inventory Tracker Tool\n", out_file_h)

    out_file_h.close()

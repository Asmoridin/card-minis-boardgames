#!/usr/bin/python3

"""
Inventory tracker and purchase selector for the Star Trek 1st Edition CCG
"""

import os
import sys

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/StarTrek1EData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('card_games/DB/StarTrek1EData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter

PRINT_SETS = ['Premiere', 'Trouble with Tribbles Starter Decks', 'Voyager', 'Deep Space 9',
    'Mirror, Mirror', 'First Contact', 'The Trouble with Tribbles', 'All Good Things', 'The Borg',
    'Blaze of Glory', 'Rules of Acquisition', 'The Motion Pictures', 'Alternate Universe', ]
VIRTUAL_SETS = ['Virtual Promos', 'Homefront III', 'Reflections', ]

VALID_TYPES = ['Ship', 'Personnel', 'Dilemma', 'Time Location', 'Objective', 'Incident',
    'Interrupt', ]
VALID_AFFILIATIONS = ['Federation', 'Klingon', 'Bajoran', 'Borg', 'Romulan', 'Dominion', 'Ferengi',
    'Kazon', 'Cardassian', 'Non-Aligned', 'Hirogen', ]

in_lines = file_h.readlines()
file_h.close()
in_lines = [line.strip() for line in in_lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
card_names = set()
for line in in_lines:
    if line == '' or line.startswith('#'):
        continue
    line = line.split('#')[0].strip() # Handle in-line comments
    try:
        card_name, card_type, card_affil, card_sets, card_numbers, card_alt_fac_num, card_max, \
            card_own = line.split(';')
    except ValueError:
        print("Issue with line:")
        print(line)
        continue
    if card_name in card_names:
        print(f"Duplicate card name: {card_name}")
    card_names.add(card_name)
    if card_type not in VALID_TYPES:
        print(f"Invalid card type: {card_type}")
        continue
    if card_type in ['Ship', 'Personnel']:
        if card_affil != '' and card_affil not in VALID_AFFILIATIONS:
            print(f"Invalid affiliation: {card_affil}")
            continue
    card_sets = card_sets.split('/')

    IS_PRINT = False
    IS_VIRTUAL = False
    for card_set in card_sets:
        if card_set not in PRINT_SETS and card_set not in VIRTUAL_SETS:
            print(f"Invalid card set: {card_set}")
        if card_set in PRINT_SETS:
            IS_PRINT = True
        if card_set in VIRTUAL_SETS:
            IS_VIRTUAL = True
    CARD_PRINT = None
    if IS_PRINT and IS_VIRTUAL:
        CARD_PRINT = 'Both'
    elif IS_PRINT:
        CARD_PRINT = 'Print'
    elif IS_VIRTUAL:
        CARD_PRINT = 'Virtual'
    else:
        print(f"Unhandled printing for card {card_name}")
        continue

    #TODO: Card Numbers
    card_max = int(card_max)
    card_own = int(card_own)
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/ST1EOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/ST1EOut.txt", 'w', encoding="UTF-8")

    double_print("Star Trek 1st Edition CCG Inventory Tracker Tool\n", out_file_h)
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} total cards - " + \
        f"{100 * TOTAL_OWN/TOTAL_MAX:.2f} percent\n", out_file_h)

    out_file_h.close()

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
    'Blaze of Glory', 'Rules of Acquisition', 'The Motion Pictures', 'Alternate Universe', 
    'The Dominion', 'Starter Deck II', 'Holodeck Adventures', 'Official Tournament Sealed Deck',
    'Enhanced First Contact']
VIRTUAL_SETS = ['Virtual Promos', 'Homefront III', 'Reflections', 'Homefront', 'Identity Crisis',
    'Homefront VI', 'Homefront V', 'Coming of Age',]

VALID_TYPES = ['Ship', 'Personnel', 'Dilemma', 'Time Location', 'Objective', 'Incident',
    'Interrupt', 'Facility', 'Mission', 'Site']
VALID_AFFILIATIONS = ['Federation', 'Klingon', 'Bajoran', 'Borg', 'Romulan', 'Dominion', 'Ferengi',
    'Kazon', 'Cardassian', 'Non-Aligned', 'Hirogen', 'Vidiian',]

class Card:
    """
    Encapsulating class for a card, to help me handle the variety of card numbers for a card.
    """
    def __init__(self, in_card_name, in_card_type, in_card_affil, in_card_sets, in_card_numbers,
        in_card_alt_fac_num):
        """
        Basic constructor of this card object
        """
        self.card_name = in_card_name
        self.card_type = in_card_type
        self.card_affil = in_card_affil
        self.card_sets = in_card_sets
        self.canon_number = min(in_card_numbers)

in_lines = file_h.readlines()
file_h.close()
in_lines = [line.strip() for line in in_lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
card_names = set()
card_lines = []
card_map = {}
for line in in_lines:
    if line == '' or line.startswith('#'):
        continue
    line = line.split('#')[0].strip() # Handle in-line comments
    try:
        card_name, card_type, card_affil, card_sets, card_numbers_str, card_alt_fac_num, card_max, \
            card_own = line.split(';')
    except ValueError:
        print("Issue with line:")
        print(line)
        continue
    if card_name in card_names and card_alt_fac_num == "":
        print(f"Duplicate card name: {card_name}")
    card_names.add(card_name)
    if card_type not in VALID_TYPES:
        print(f"Invalid card type: {card_type}")
        continue
    if card_type in ['Ship', 'Personnel', 'Facility']:
        if card_affil not in VALID_AFFILIATIONS:
            print(f"Invalid affiliation: {card_affil}")
            continue
    if card_type in ['Mission', 'Dilemma']:
        if card_affil not in ['Planet', 'Space', 'Dual']:
            print(f"Possibly mis-typed card: {card_name}")
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
    CARD_PRINT = []
    if IS_PRINT:
        CARD_PRINT.append('Print')
    elif IS_VIRTUAL:
        CARD_PRINT.append('Virtual')

    card_numbers = []
    for card_num in card_numbers_str.split(','):
        card_num = int(card_num)
        card_numbers.append(card_num)
    alt_numbers = []
    if card_alt_fac_num != "":
        for card_num in card_alt_fac_num.split(','):
            card_num = int(card_num)
            alt_numbers.append(card_num)

    card_max = int(card_max)
    card_own = int(card_own)
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    card_lines.append([card_name, card_type, card_affil, card_sets, card_numbers, \
        alt_numbers, card_max, card_own])

print(card_lines)

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/ST1EOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/ST1EOut.txt", 'w', encoding="UTF-8")

    double_print("Star Trek 1st Edition CCG Inventory Tracker Tool\n", out_file_h)
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} total cards - " + \
        f"{100 * TOTAL_OWN/TOTAL_MAX:.2f} percent\n", out_file_h)

    out_file_h.close()
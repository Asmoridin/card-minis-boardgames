#!/usr/bin/python

"""
Collection tracker/management for Magic: The Gathering
"""

import os
import re
import sys

sys.path.append('.')
from utils.output_utils import double_print
from utils.sort_and_filter import sort_and_filter
from card_games.Libraries import mtg_sets

GAME_NAME = "Magic: The Gathering"

file_h = open('card_games/DB/MTGCardData.txt', 'r', encoding="UTF-8")
restr_file_h = open('card_games/DB/MTGRestrictions.txt', 'r', encoding="UTF-8")

def parse_restrictions(restr_lines):
    """
    Create a list of restrictions for each card, if relevant
    """
    return_dict = {}
    for rest_line in restr_lines:
        this_card_name, card_restrictions = rest_line.strip().split(';')
        return_dict[this_card_name] = {}
        for restriction in card_restrictions.split('/'):
            this_format, bnr = restriction.split('-')
            if this_format not in ['Legacy', 'Vintage', 'Commander', 'Pauper']:
                print("Unknown format: " + this_format)
            if bnr not in ['Banned', 'Restricted']:
                print("Unknown status: " + bnr)
            return_dict[this_card_name][this_format] = bnr
    return return_dict

def parse_sets(this_card_name, card_set_string, card_restrictions):
    """
    The heavy lifting function of this module, where I go through and figure out rarites, sets,
    formats, and anything else
    """
    ret_sets = []
    ret_rarities = set()
    ret_formats = {"Commander": 1, "Vintage": 4, "Legacy": 4}
    this_card_max = 1
    for card_set in card_set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", card_set)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            if this_set in mtg_sets.LEGACY_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
            elif this_set in mtg_sets.ARENA_SETS:
                pass # We don't care one bit about Arena sets
            elif this_set in mtg_sets.MTGO_SETS:
                # We don't track the set, but the rarity matters
                ret_rarities.add(this_set_rarity)
            elif this_set in mtg_sets.STANDARD_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
                ret_formats['Standard'] = 4
                ret_formats['Pioneer'] = 4
                ret_formats['Modern'] = 4
            elif this_set in mtg_sets.PIONEER_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
                ret_formats['Pioneer'] = 4
                ret_formats['Modern'] = 4
            elif this_set in mtg_sets.MODERN_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
                ret_formats['Modern'] = 4
            else:
                print("[" + this_card_name + "] Handle: " + this_set)
        else:
            print("[" + this_card_name + "] Issue with: " + card_set)
    if 'Common' in ret_rarities or 'Land' in ret_rarities:
        ret_formats['Pauper'] = 4
    if card_restrictions:
        for restriction_format, restriction_bnr in card_restrictions.items():
            if restriction_bnr == 'Banned':
                del ret_formats[restriction_format]
            elif restriction_bnr == 'Restricted':
                ret_formats[restriction_format] = 1
            else:
                print(restriction_format)
                print(restriction_bnr)
    if len(ret_formats) == 1:
        ret_formats = {"Vintage": 1}
    for _, format_qty in ret_formats.items():
        this_card_max = max(this_card_max, format_qty)
    ret_rarities = list(ret_rarities)
    return(ret_sets, ret_rarities, ret_formats, this_card_max)

def validate_colors(in_colors):
    """
    Takes in a string of colors, and returns a list with the full color names
    """
    ret_colors = []
    color_map = {'C':'Colorless', 'B':'Black', 'U':'Blue', 'R':'Red', 'W':'White',
        'G':'Green'}
    for color in in_colors.split('/'):
        if color not in color_map:
            print("Invalid color: " + color)
        else:
            ret_colors.append(color_map[color])
    return ret_colors

def validate_types(card_type_string):
    """
    Take a string of card types, and return both the card type(s) and subtype(s)
    """
    ret_type = []
    ret_subtype = []
    if '—' in card_type_string:
        types, subtypes = card_type_string.split(' — ')
        types = types.strip()
        subtypes = subtypes.strip()
    else:
        types = card_type_string
        subtypes = ''
    if types == 'Basic Land':
        ret_type.append(types)
        types = ''
    for check_type in types.split(' '):
        if check_type == '':
            continue
        if check_type in ['Artifact', 'Creature', 'Enchantment', 'Sorcery', "Instant"]:
            ret_type.append(check_type)
        else:
            print("Unknown type: " + check_type)
    for check_type in subtypes.split(' '):
        ret_subtype.append(check_type)
    return(ret_type, ret_subtype)

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

restrictions = parse_restrictions(restr_file_h.readlines())
restr_file_h.close()

TOTAL_OWN = 0
TOTAL_MAX = 0
raw_list = []
card_names = set()
for line in lines:
    if line == '' or line.startswith('#'):
        continue
    try:
        card_name, card_type, card_colors, card_sets, card_qty = line.split(';')
    except ValueError:
        print("Error in line:")
        print(line)
        continue
    if card_name in card_names:
        print(f"Duplicate: {card_name}")
    card_names.add(card_name)
    card_qty = int(card_qty)
    card_colors = validate_colors(card_colors)
    card_type, card_subtype = validate_types(card_type)
    card_sets, card_rarities, card_formats, CARD_MAX = parse_sets(card_name, card_sets, \
        restrictions.get(card_name))
    if 'Basic Land' in card_type:
        for card_format in card_formats:
            card_formats[card_format] = 20
            CARD_MAX = 20
    TOTAL_MAX += CARD_MAX
    TOTAL_OWN += card_qty
    raw_list.append((card_name, card_type, card_subtype, card_colors, card_sets, card_rarities, \
        card_formats, card_qty, CARD_MAX))

# Get data for Vintage
vintage_list = []
VINTAGE_OWN = 0
VINTAGE_TOTAL = 0
for card in raw_list:
    if 'Vintage' in card[6]:
        vintage_list.append(card)
        VINTAGE_TOTAL += card[6]['Vintage']
        VINTAGE_OWN += min(card[7], card[6]['Vintage'])
VINTAGE_CARDS = len(vintage_list)

vintage_set, filtered_list = sort_and_filter(vintage_list, 4)
vintage_type, filtered_list = sort_and_filter(filtered_list, 1)
if vintage_type == 'Creature':
    _, filtered_list = sort_and_filter(filtered_list, 2)
vintage_color, filtered_list = sort_and_filter(filtered_list, 3)
vintage_rarity, filtered_list = sort_and_filter(filtered_list, 5)
vintage_name, filtered_list = sort_and_filter(filtered_list, 0)
vintage_item = filtered_list[0]

# Get data for Legacy
legacy_list = []
LEGACY_OWN = 0
LEGACY_TOTAL = 0
for card in raw_list:
    if 'Legacy' in card[6]:
        legacy_list.append(card)
        LEGACY_TOTAL += card[6]['Legacy']
        LEGACY_OWN += min(card[7], card[6]['Legacy'])
LEGACY_CARDS = len(legacy_list)

legacy_set, filtered_list = sort_and_filter(legacy_list, 4)
legacy_type, filtered_list = sort_and_filter(filtered_list, 1)
if legacy_type == 'Creature':
    _, filtered_list = sort_and_filter(filtered_list, 2)
legacy_color, filtered_list = sort_and_filter(filtered_list, 3)
legacy_rarity, filtered_list = sort_and_filter(filtered_list, 5)
legacy_name, filtered_list = sort_and_filter(filtered_list, 0)
legacy_item = filtered_list[0]

# Get data for Commander
commander_list = []
COMMANDER_OWN = 0
COMMANDER_TOTAL = 0
for card in raw_list:
    if 'Commander' in card[6]:
        commander_list.append(card)
        COMMANDER_TOTAL += card[6]['Commander']
        COMMANDER_OWN += min(card[7], card[6]['Commander'])
COMMANDER_CARDS = len(commander_list)

commander_set, filtered_list = sort_and_filter(commander_list, 4)
commander_type, filtered_list = sort_and_filter(filtered_list, 1)
if commander_type == 'Creature':
    _, filtered_list = sort_and_filter(filtered_list, 2)
commander_color, filtered_list = sort_and_filter(filtered_list, 3)
commander_rarity, filtered_list = sort_and_filter(filtered_list, 5)
commander_name, filtered_list = sort_and_filter(filtered_list, 0)
commander_item = filtered_list[0]

# Get data for Pioneer
pioneer_list = []
PIONEER_OWN = 0
PIONEER_TOTAL = 0
for card in raw_list:
    if 'Pioneer' in card[6]:
        pioneer_list.append(card)
        PIONEER_TOTAL += card[6]['Pioneer']
        PIONEER_OWN += min(card[7], card[6]['Pioneer'])
PIONEER_CARDS = len(pioneer_list)

pioneer_set, filtered_list = sort_and_filter(pioneer_list, 4)
pioneer_type, filtered_list = sort_and_filter(filtered_list, 1)
if pioneer_type == 'Creature':
    _, filtered_list = sort_and_filter(filtered_list, 2)
pioneer_color, filtered_list = sort_and_filter(filtered_list, 3)
pioneer_rarity, filtered_list = sort_and_filter(filtered_list, 5)
pioneer_name, filtered_list = sort_and_filter(filtered_list, 0)
pioneer_item = filtered_list[0]

# Get data for Modern
modern_list = []
MODERN_OWN = 0
MODERN_TOTAL = 0
for card in raw_list:
    if 'Modern' in card[6]:
        modern_list.append(card)
        MODERN_TOTAL += card[6]['Modern']
        MODERN_OWN += min(card[7], card[6]['Modern'])
MODERN_CARDS = len(modern_list)

modern_set, filtered_list = sort_and_filter(modern_list, 4)
modern_type, filtered_list = sort_and_filter(filtered_list, 1)
if modern_type == 'Creature':
    _, filtered_list = sort_and_filter(filtered_list, 2)
modern_color, filtered_list = sort_and_filter(filtered_list, 3)
modern_rarity, filtered_list = sort_and_filter(filtered_list, 5)
modern_name, filtered_list = sort_and_filter(filtered_list, 0)
modern_item = filtered_list[0]

# Get data for Standard
standard_list = []
STANDARD_OWN = 0
STANDARD_TOTAL = 0
for card in raw_list:
    if 'Standard' in card[6]:
        standard_list.append(card)
        STANDARD_TOTAL += card[6]['Standard']
        STANDARD_OWN += min(card[7], card[6]['Standard'])
STANDARD_CARDS = len(standard_list)

standard_set, filtered_list = sort_and_filter(standard_list, 4)
standard_type, filtered_list = sort_and_filter(filtered_list, 1)
if standard_type == 'Creature':
    _, filtered_list = sort_and_filter(filtered_list, 2)
standard_color, filtered_list = sort_and_filter(filtered_list, 3)
standard_rarity, filtered_list = sort_and_filter(filtered_list, 5)
standard_name, filtered_list = sort_and_filter(filtered_list, 0)
standard_item = filtered_list[0]

# Get data for Pauper
pauper_list = []
PAUPER_OWN = 0
PAUPER_TOTAL = 0
for card in raw_list:
    if 'Pauper' in card[6]:
        pauper_list.append(card)
        PAUPER_TOTAL += card[6]['Pauper']
        PAUPER_OWN += min(card[7], card[6]['Pauper'])
PAUPER_CARDS = len(pauper_list)

pauper_set, filtered_list = sort_and_filter(pauper_list, 4)
pauper_type, filtered_list = sort_and_filter(filtered_list, 1)
if pauper_type == 'Creature':
    _, filtered_list = sort_and_filter(filtered_list, 2)
pauper_color, filtered_list = sort_and_filter(filtered_list, 3)
pauper_rarity, filtered_list = sort_and_filter(filtered_list, 5)
pauper_name, filtered_list = sort_and_filter(filtered_list, 0)
pauper_item = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/MTGOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/MTGOut.txt", 'w', encoding="UTF-8")

    double_print(f"Tracking {len(raw_list)} cards.", out_file_h)
    SUMMARY_STRING = f"Have {TOTAL_OWN} out of {TOTAL_MAX} total cards for a playset " \
        f"- {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(SUMMARY_STRING, out_file_h)

    double_print("\n*** VINTAGE ***", out_file_h)
    double_print(f"There are {VINTAGE_CARDS} Vintage legal cards", out_file_h)
    VINT_STR = f"Have {VINTAGE_OWN} out of {VINTAGE_TOTAL} - " \
        f"{100* VINTAGE_OWN/VINTAGE_TOTAL:.2f} percent of a playset"
    double_print(VINT_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {vintage_type} from {vintage_set} - {vintage_name}. " + \
        f"I own {vintage_item[7]} of {vintage_item[6]['Vintage']}"
    double_print(PURCH_STR, out_file_h)

    double_print("\n*** LEGACY ***", out_file_h)
    double_print(f"There are {LEGACY_CARDS} Legacy legal cards", out_file_h)
    LEGACY_STR = f"Have {LEGACY_OWN} out of {LEGACY_TOTAL} - " \
        f"{100* LEGACY_OWN/LEGACY_TOTAL:.2f} percent of a playset"
    double_print(LEGACY_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {legacy_type} from {legacy_set} - {legacy_name}. " + \
        f"I own {legacy_item[7]} of {legacy_item[6]['Legacy']}"
    double_print(PURCH_STR, out_file_h)

    double_print("\n*** COMMANDER ***", out_file_h)
    double_print(f"There are {COMMANDER_CARDS} Commander legal cards", out_file_h)
    COMMANDER_STR = f"Have {COMMANDER_OWN} out of {COMMANDER_TOTAL} - " \
        f"{100* COMMANDER_OWN/COMMANDER_TOTAL:.2f} percent of a playset"
    double_print(COMMANDER_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {commander_type} from {commander_set} - {commander_name}" + \
        f". I own {commander_item[7]} of {commander_item[6]['Commander']}"
    double_print(PURCH_STR, out_file_h)

    double_print("\n*** PIONEER ***", out_file_h)
    double_print(f"There are {PIONEER_CARDS} Pioneer legal cards", out_file_h)
    PIONEER_STR = f"Have {PIONEER_OWN} out of {PIONEER_TOTAL} - " \
        f"{100* PIONEER_OWN/PIONEER_TOTAL:.2f} percent of a playset"
    double_print(PIONEER_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {pioneer_type} from {pioneer_set} - {pioneer_name}" + \
        f". I own {pioneer_item[7]} of {pioneer_item[6]['Pioneer']}"
    double_print(PURCH_STR, out_file_h)

    double_print("\n*** MODERN ***", out_file_h)
    double_print(f"There are {MODERN_CARDS} Modern legal cards", out_file_h)
    MODERN_STR = f"Have {MODERN_OWN} out of {MODERN_TOTAL} - " \
        f"{100* MODERN_OWN/MODERN_TOTAL:.2f} percent of a playset"
    double_print(MODERN_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {modern_type} from {modern_set} - {modern_name}" + \
        f". I own {modern_item[7]} of {modern_item[6]['Modern']}"
    double_print(PURCH_STR, out_file_h)

    double_print("\n*** STANDARD ***", out_file_h)
    double_print(f"There are {STANDARD_CARDS} Standard legal cards", out_file_h)
    STANDARD_STR = f"Have {STANDARD_OWN} out of {STANDARD_TOTAL} - " \
        f"{100* STANDARD_OWN/STANDARD_TOTAL:.2f} percent of a playset"
    double_print(STANDARD_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {standard_type} from {standard_set} - {standard_name}" + \
        f". I own {standard_item[7]} of {standard_item[6]['Standard']}"
    double_print(PURCH_STR, out_file_h)

    double_print("\n*** PAUPER ***", out_file_h)
    double_print(f"There are {PAUPER_CARDS} Pauper legal cards", out_file_h)
    PAUPER_STR = f"Have {PAUPER_OWN} out of {PAUPER_TOTAL} - " \
        f"{100* PAUPER_OWN/PAUPER_TOTAL:.2f} percent of a playset"
    double_print(PAUPER_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {pauper_type} from {pauper_set} - {pauper_name}" + \
        f". I own {pauper_item[7]} of {pauper_item[6]['Pauper']}"
    double_print(PURCH_STR, out_file_h)
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
DECK_DIR = "card_games/DB/Decks/MTG"

def read_decks(deck_format):
    """
    Takes in a format, and returns a list of dicts of all my stored decks for that format
    """
    ret_list = []
    if deck_format in os.listdir(DECK_DIR):
        for deck_file in os.listdir(DECK_DIR + '/' + deck_format):
            this_deck = {}
            deck_fh = open(DECK_DIR + '/' + deck_format + '/' + deck_file, 'r', encoding='UTF-8')
            deck_lines = deck_fh.readlines()
            deck_fh.close()
            deck_lines = [line.strip() for line in deck_lines]
            for deck_line in deck_lines:
                if deck_line.startswith('//') or deck_line == '':
                    continue
                deck_card_qty = int(deck_line.split(' ')[0])
                deck_card_name = ' '.join(deck_line.split(' ')[1:])
                if deck_card_name not in this_deck:
                    this_deck[deck_card_name] = 0
                this_deck[deck_card_name] += deck_card_qty
            ret_list.append(this_deck)
    return ret_list

def check_decks(list_of_decks, list_of_cards):
    """
    Given:
    - a list of deck dicts, and a list of relevant card tuples
    Return:
    - a list of tuples that are [MISSING_NO], [MISSING_CARDS]
    """
    ret_list = []
    # First, construct a dict of the cards in the format
    inventory_dict = {}
    for in_card in list_of_cards:
        inventory_dict[in_card[0]] = in_card[7]
    for deck in list_of_decks:
        this_deck_missing = 0
        this_deck_missing_cards = {}
        for this_card, card_count in deck.items():
            if this_card in inventory_dict:
                if card_count > inventory_dict[this_card]:
                    this_deck_missing += card_count - inventory_dict[this_card]
                    this_deck_missing_cards[this_card] = card_count - inventory_dict[this_card]
            else:
                print(f"Missing card {this_card}")
                this_deck_missing += card_count
                this_deck_missing_cards[this_card] = card_count
        ret_list.append((this_deck_missing, this_deck_missing_cards))
    return ret_list

def aggregate_most_needed(deck_lists):
    """
    From a list of dicts, of cards missing for decks, generate a list of tuples of those cards
    and a total weight of said cards
    """
    ret_list = []
    temp_dict = {}
    for deck_list in deck_lists:
        for deck_card, deck_card_qty in deck_list[1].items():
            if deck_card not in temp_dict:
                temp_dict[deck_card] = 0
            temp_dict[deck_card] += deck_card_qty
    for temp_card, temp_card_qty in temp_dict.items():
        ret_list.append((temp_card, temp_card_qty))
    return ret_list

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
            if this_format not in ['Legacy', 'Vintage', 'Commander', 'Pauper', 'Modern',
                    'Standard', 'Pioneer', ]:
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
            elif this_set in mtg_sets.ARENA_SETS or this_set in mtg_sets.NON_SETS:
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
    if len(ret_formats) == 0:
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
    if '-' in card_type_string:
        types, subtypes = card_type_string.split(' - ')
        types = types.strip()
        subtypes = subtypes.strip()
    else:
        types = card_type_string
        subtypes = ''
    if types == 'Basic Land' or types in 'World Enchantment':
        ret_type.append(types)
        types = ''
    for check_type in types.split(' '):
        if check_type == '':
            continue
        if check_type in ['Artifact', 'Creature', 'Enchantment', 'Sorcery', "Instant",
                "Legendary", 'Land', 'Planeswalker', ]:
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
creature_types = {}
SET_CHECK = 0
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
    card_type = card_type.replace('—', '-')
    card_type, card_subtype = validate_types(card_type)
    if 'Creature' in card_type:
        for subtype in card_subtype:
            if subtype not in creature_types:
                creature_types[subtype] = 0
            creature_types[subtype] += 1
    card_sets, card_rarities, card_formats, CARD_MAX = parse_sets(card_name, card_sets, \
        restrictions.get(card_name))
    if 'Legends' in card_sets:
        SET_CHECK += 1
    if 'Basic Land' in card_type:
        for card_format in card_formats:
            card_formats[card_format] = 30
            CARD_MAX = 30
    TOTAL_MAX += CARD_MAX
    TOTAL_OWN += card_qty
    raw_list.append((card_name, card_type, card_subtype, card_colors, card_sets, card_rarities, \
        card_formats, card_qty, CARD_MAX))

FORMAT_LIST = []

# Get data for Vintage
vintage_list = []
VINTAGE_OWN = 0
VINTAGE_TOTAL = 0
for card in raw_list:
    if 'Vintage' in card[6]:
        vintage_list.append(card)
        VINTAGE_TOTAL += card[6]['Vintage']
        VINTAGE_OWN += min(card[7], card[6]['Vintage'])
    else:
        print(card)
VINTAGE_CARDS = len(vintage_list)
FORMAT_LIST.append(("Vintage", VINTAGE_OWN, VINTAGE_TOTAL))

vintage_set, filtered_list = sort_and_filter(vintage_list, 4)
vintage_type, filtered_list = sort_and_filter(filtered_list, 1)
if vintage_type == 'Creature' or vintage_type == 'Planeswalker':
    _, filtered_list = sort_and_filter(filtered_list, 2)
vintage_color, filtered_list = sort_and_filter(filtered_list, 3)
vintage_rarity, filtered_list = sort_and_filter(filtered_list, 5)
vintage_name, filtered_list = sort_and_filter(filtered_list, 0)
vintage_item = filtered_list[0]

vintage_decks = read_decks('Vintage')
vint_decks_minus_own = check_decks(vintage_decks, vintage_list)
vint_most_needed = aggregate_most_needed(vint_decks_minus_own)
vint_most_needed = sorted(vint_most_needed, key=lambda x:(-1 * x[1], x[0]))
vint_decks_minus_own = sorted(vint_decks_minus_own, key=lambda x:x[0])

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
FORMAT_LIST.append(("Legacy", LEGACY_OWN, LEGACY_TOTAL))

legacy_set, filtered_list = sort_and_filter(legacy_list, 4)
legacy_type, filtered_list = sort_and_filter(filtered_list, 1)
if legacy_type == 'Creature' or legacy_type == 'Planeswalker':
    _, filtered_list = sort_and_filter(filtered_list, 2)
legacy_color, filtered_list = sort_and_filter(filtered_list, 3)
legacy_rarity, filtered_list = sort_and_filter(filtered_list, 5)
legacy_name, filtered_list = sort_and_filter(filtered_list, 0)
legacy_item = filtered_list[0]

legacy_decks = read_decks('Legacy')
legacy_decks_minus_own = check_decks(legacy_decks, legacy_list)
legacy_most_needed = aggregate_most_needed(legacy_decks_minus_own)
legacy_most_needed = sorted(legacy_most_needed, key=lambda x:(-1 * x[1], x[0]))
legacy_decks_minus_own = sorted(legacy_decks_minus_own, key=lambda x:x[0])

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
FORMAT_LIST.append(("Commander", COMMANDER_OWN, COMMANDER_TOTAL))

commander_set, filtered_list = sort_and_filter(commander_list, 4)
commander_type, filtered_list = sort_and_filter(filtered_list, 1)
if commander_type == 'Creature' or commander_type == 'Planeswalker':
    _, filtered_list = sort_and_filter(filtered_list, 2)
commander_color, filtered_list = sort_and_filter(filtered_list, 3)
commander_rarity, filtered_list = sort_and_filter(filtered_list, 5)
commander_name, filtered_list = sort_and_filter(filtered_list, 0)
commander_item = filtered_list[0]

commander_decks = read_decks('Commander')
comm_decks_minus_own = check_decks(commander_decks, commander_list)
comm_most_needed = aggregate_most_needed(comm_decks_minus_own)
comm_most_needed = sorted(comm_most_needed, key=lambda x:(-1 * x[1], x[0]))
comm_decks_minus_own = sorted(comm_decks_minus_own, key=lambda x:x[0])

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
FORMAT_LIST.append(("Pioneer", PIONEER_OWN, PIONEER_TOTAL))

pioneer_set, filtered_list = sort_and_filter(pioneer_list, 4)
pioneer_type, filtered_list = sort_and_filter(filtered_list, 1)
if pioneer_type == 'Creature' or pioneer_type == 'Planeswalker':
    _, filtered_list = sort_and_filter(filtered_list, 2)
pioneer_color, filtered_list = sort_and_filter(filtered_list, 3)
pioneer_rarity, filtered_list = sort_and_filter(filtered_list, 5)
pioneer_name, filtered_list = sort_and_filter(filtered_list, 0)
pioneer_item = filtered_list[0]

pioneer_decks = read_decks('Pioneer')
pioneer_decks_minus_own = check_decks(pioneer_decks, pioneer_list)
pioneer_most_needed = aggregate_most_needed(pioneer_decks_minus_own)
pioneer_most_needed = sorted(pioneer_most_needed, key=lambda x:(-1 * x[1], x[0]))
pioneer_decks_minus_own = sorted(pioneer_decks_minus_own, key=lambda x:x[0])

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
FORMAT_LIST.append(("Modern", MODERN_OWN, MODERN_TOTAL))

modern_set, filtered_list = sort_and_filter(modern_list, 4)
modern_type, filtered_list = sort_and_filter(filtered_list, 1)
if modern_type == 'Creature' or modern_type == 'Planeswalker':
    _, filtered_list = sort_and_filter(filtered_list, 2)
modern_color, filtered_list = sort_and_filter(filtered_list, 3)
modern_rarity, filtered_list = sort_and_filter(filtered_list, 5)
modern_name, filtered_list = sort_and_filter(filtered_list, 0)
modern_item = filtered_list[0]

modern_decks = read_decks('Modern')
modern_decks_minus_own = check_decks(modern_decks, modern_list)
modern_most_needed = aggregate_most_needed(modern_decks_minus_own)
modern_most_needed = sorted(modern_most_needed, key=lambda x:(-1 * x[1], x[0]))
modern_decks_minus_own = sorted(modern_decks_minus_own, key=lambda x:x[0])

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
FORMAT_LIST.append(("Standard", STANDARD_OWN, STANDARD_TOTAL))

standard_set, filtered_list = sort_and_filter(standard_list, 4)
standard_type, filtered_list = sort_and_filter(filtered_list, 1)
if standard_type == 'Creature' or standard_type == 'Planeswalker':
    _, filtered_list = sort_and_filter(filtered_list, 2)
standard_color, filtered_list = sort_and_filter(filtered_list, 3)
standard_rarity, filtered_list = sort_and_filter(filtered_list, 5)
standard_name, filtered_list = sort_and_filter(filtered_list, 0)
standard_item = filtered_list[0]

standard_decks = read_decks('Standard')
standard_decks_minus_own = check_decks(standard_decks, standard_list)
standard_most_needed = aggregate_most_needed(standard_decks_minus_own)
standard_most_needed = sorted(standard_most_needed, key=lambda x:(-1 * x[1], x[0]))
standard_decks_minus_own = sorted(standard_decks_minus_own, key=lambda x:x[0])

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
FORMAT_LIST.append(("Pauper", PAUPER_OWN, PAUPER_TOTAL))

pauper_set, filtered_list = sort_and_filter(pauper_list, 4)
pauper_type, filtered_list = sort_and_filter(filtered_list, 1)
if pauper_type == 'Creature' or pauper_type == 'Planeswalker':
    _, filtered_list = sort_and_filter(filtered_list, 2)
pauper_color, filtered_list = sort_and_filter(filtered_list, 3)
pauper_rarity, filtered_list = sort_and_filter(filtered_list, 5)
pauper_name, filtered_list = sort_and_filter(filtered_list, 0)
pauper_item = filtered_list[0]

pauper_decks = read_decks('Pauper')
pauper_decks_minus_own = check_decks(pauper_decks, pauper_list)
pauper_most_needed = aggregate_most_needed(pauper_decks_minus_own)
pauper_most_needed = sorted(pauper_most_needed, key=lambda x:(-1 * x[1], x[0]))
pauper_decks_minus_own = sorted(pauper_decks_minus_own, key=lambda x:x[0])

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/MTGOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/MTGOut.txt", 'w', encoding="UTF-8")

    double_print(f"Tracking {len(raw_list)} cards.", out_file_h)
    SUMMARY_STRING = f"Have {TOTAL_OWN} out of {TOTAL_MAX} total cards for a playset " \
        f"- {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(SUMMARY_STRING, out_file_h)

    # Vintage
    double_print("\n*** VINTAGE ***", out_file_h)
    double_print(f"There are {VINTAGE_CARDS} Vintage legal cards", out_file_h)
    VINT_STR = f"Have {VINTAGE_OWN} out of {VINTAGE_TOTAL} - " \
        f"{100* VINTAGE_OWN/VINTAGE_TOTAL:.2f} percent of a playset"
    double_print(VINT_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {vintage_type} from {vintage_set} - {vintage_name}. " + \
        f"I own {vintage_item[7]} of {vintage_item[6]['Vintage']}"
    double_print(PURCH_STR, out_file_h)

    double_print(f"\nClosest deck to completion is at {vint_decks_minus_own[0][0]} " + \
        "cards.", out_file_h)
    double_print(str(vint_decks_minus_own[0][1]), out_file_h)

    double_print("\nMost needed cards are:", out_file_h)
    for card_tuple in vint_most_needed[:10]:
        double_print(f" - {card_tuple[0]}: {card_tuple[1]}", out_file_h)

    # Legacy
    double_print("\n*** LEGACY ***", out_file_h)
    double_print(f"There are {LEGACY_CARDS} Legacy legal cards", out_file_h)
    LEGACY_STR = f"Have {LEGACY_OWN} out of {LEGACY_TOTAL} - " \
        f"{100* LEGACY_OWN/LEGACY_TOTAL:.2f} percent of a playset"
    double_print(LEGACY_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {legacy_type} from {legacy_set} - {legacy_name}. " + \
        f"I own {legacy_item[7]} of {legacy_item[6]['Legacy']}"
    double_print(PURCH_STR, out_file_h)

    double_print(f"\nClosest deck to completion is at {legacy_decks_minus_own[0][0]} " + \
        "cards.", out_file_h)
    double_print(str(legacy_decks_minus_own[0][1]), out_file_h)

    double_print("\nMost needed cards are:", out_file_h)
    for card_tuple in legacy_most_needed[:10]:
        double_print(f" - {card_tuple[0]}: {card_tuple[1]}", out_file_h)

    # Commander
    double_print("\n*** COMMANDER ***", out_file_h)
    double_print(f"There are {COMMANDER_CARDS} Commander legal cards", out_file_h)
    COMMANDER_STR = f"Have {COMMANDER_OWN} out of {COMMANDER_TOTAL} - " \
        f"{100* COMMANDER_OWN/COMMANDER_TOTAL:.2f} percent of a playset"
    double_print(COMMANDER_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {commander_type} from {commander_set} - {commander_name}" + \
        f". I own {commander_item[7]} of {commander_item[6]['Commander']}"
    double_print(PURCH_STR, out_file_h)

    double_print(f"\nClosest deck to completion is at {comm_decks_minus_own[0][0]} " + \
        "cards.", out_file_h)
    double_print(str(comm_decks_minus_own[0][1]), out_file_h)

    double_print("\nMost needed cards are:", out_file_h)
    for card_tuple in comm_most_needed[:10]:
        double_print(f" - {card_tuple[0]}: {card_tuple[1]}", out_file_h)

    # Modern
    double_print("\n*** MODERN ***", out_file_h)
    double_print(f"There are {MODERN_CARDS} Modern legal cards", out_file_h)
    MODERN_STR = f"Have {MODERN_OWN} out of {MODERN_TOTAL} - " \
        f"{100* MODERN_OWN/MODERN_TOTAL:.2f} percent of a playset"
    double_print(MODERN_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {modern_type} from {modern_set} - {modern_name}" + \
        f". I own {modern_item[7]} of {modern_item[6]['Modern']}"
    double_print(PURCH_STR, out_file_h)

    double_print(f"\nClosest deck to completion is at {modern_decks_minus_own[0][0]} " + \
        "cards.", out_file_h)
    double_print(str(modern_decks_minus_own[0][1]), out_file_h)

    double_print("\nMost needed cards are:", out_file_h)
    for card_tuple in modern_most_needed[:10]:
        double_print(f" - {card_tuple[0]}: {card_tuple[1]}", out_file_h)

    # Pioneer
    double_print("\n*** PIONEER ***", out_file_h)
    double_print(f"There are {PIONEER_CARDS} Pioneer legal cards", out_file_h)
    PIONEER_STR = f"Have {PIONEER_OWN} out of {PIONEER_TOTAL} - " \
        f"{100* PIONEER_OWN/PIONEER_TOTAL:.2f} percent of a playset"
    double_print(PIONEER_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {pioneer_type} from {pioneer_set} - {pioneer_name}" + \
        f". I own {pioneer_item[7]} of {pioneer_item[6]['Pioneer']}"
    double_print(PURCH_STR, out_file_h)

    double_print(f"\nClosest deck to completion is at {pioneer_decks_minus_own[0][0]} " + \
        "cards.", out_file_h)
    double_print(str(pioneer_decks_minus_own[0][1]), out_file_h)

    double_print("\nMost needed cards are:", out_file_h)
    for card_tuple in pioneer_most_needed[:10]:
        double_print(f" - {card_tuple[0]}: {card_tuple[1]}", out_file_h)

    # Standard
    double_print("\n*** STANDARD ***", out_file_h)
    double_print(f"There are {STANDARD_CARDS} Standard legal cards", out_file_h)
    STANDARD_STR = f"Have {STANDARD_OWN} out of {STANDARD_TOTAL} - " \
        f"{100* STANDARD_OWN/STANDARD_TOTAL:.2f} percent of a playset"
    double_print(STANDARD_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {standard_type} from {standard_set} - {standard_name}" + \
        f". I own {standard_item[7]} of {standard_item[6]['Standard']}"
    double_print(PURCH_STR, out_file_h)

    double_print(f"\nClosest deck to completion is at {standard_decks_minus_own[0][0]} " + \
        "cards.", out_file_h)
    double_print(str(standard_decks_minus_own[0][1]), out_file_h)

    double_print("\nMost needed cards are:", out_file_h)
    for card_tuple in standard_most_needed[:10]:
        double_print(f" - {card_tuple[0]}: {card_tuple[1]}", out_file_h)

    # Pauper
    double_print("\n*** PAUPER ***", out_file_h)
    double_print(f"There are {PAUPER_CARDS} Pauper legal cards", out_file_h)
    PAUPER_STR = f"Have {PAUPER_OWN} out of {PAUPER_TOTAL} - " \
        f"{100* PAUPER_OWN/PAUPER_TOTAL:.2f} percent of a playset"
    double_print(PAUPER_STR, out_file_h)

    PURCH_STR = f"Chosen card is a(n) {pauper_type} from {pauper_set} - {pauper_name}" + \
        f". I own {pauper_item[7]} of {pauper_item[6]['Pauper']}"
    double_print(PURCH_STR, out_file_h)

    double_print(f"\nClosest deck to completion is at {pauper_decks_minus_own[0][0]} " + \
        "cards.", out_file_h)
    double_print(str(pauper_decks_minus_own[0][1]), out_file_h)

    double_print("\nMost needed cards are:", out_file_h)
    for card_tuple in pauper_most_needed[:10]:
        double_print(f" - {card_tuple[0]}: {card_tuple[1]}", out_file_h)

    double_print("\n*** OTHER DATA ***", out_file_h)
    double_print("Most common creature types:", out_file_h)
    creature_types = sorted(creature_types.items(), key=lambda x:(-1 * x[1], x[0]))
    for creature_tuple in creature_types[:100]:
        double_print(f"- {creature_tuple[0]}: {creature_tuple[1]}", out_file_h)

    double_print("\nPercentages ordered by format:", out_file_h)
    FORMAT_LIST = sorted(FORMAT_LIST, key=lambda x:(x[1]/x[2], x[0]), reverse=True)
    for print_format in FORMAT_LIST:
        double_print(f"{print_format[0]}: {100 * print_format[1]/print_format[2]:.2f}", out_file_h)

    print(SET_CHECK)
    print("Above should be 310 for Legends")

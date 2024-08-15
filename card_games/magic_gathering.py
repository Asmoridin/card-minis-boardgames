#!/usr/bin/python

"""
Collection tracker/management for Magic: The Gathering
"""

import os
import re
import sys

GAME_NAME = "Magic: The Gathering"

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/MTGCardData.txt', 'r', encoding="UTF-8")
    restr_file_h = open('card_games/DB/MTGRestrictions.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
    from card_games.Libraries import mtg_sets
else:
    file_h = open('DB/MTGCardData.txt', 'r', encoding="UTF-8")
    restr_file_h = open('DB/MTGRestrictions.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
    from Libraries import mtg_sets

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
            if this_format not in ['Legacy', 'Vintage']:
                print("Unknown format: " + this_format)
            if bnr not in ['Banned', 'Restricted', 'Commander']:
                print("Unknown status: " + bnr)
            return_dict[this_card_name][this_format] = bnr
    return return_dict

def parse_sets(card_name, card_set_string, card_restrictions):
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
            elif this_set in mtg_sets.MTGO_SETS:
                # We don't track the set, but the rarity matters
                ret_rarities.add(this_set_rarity)
            else:
                print("[" + card_name + "] Handle: " + this_set)
        else:
            print("[" + card_name + "] Issue with: " + card_set)
    if card_restrictions:
        for restriction_format, restriction_bnr in card_restrictions.items():
            if restriction_bnr == 'Banned':
                del ret_formats[restriction_format]
            elif restriction_bnr == 'Restricted':
                ret_formats[restriction_format] = 1
            else:
                print(restriction_format)
                print(restriction_bnr)
    return(ret_sets, ret_rarities, ret_formats, this_card_max)

def validate_colors(in_colors):
    """
    Takes in a string of colors, and returns a list with the full color names
    """
    ret_colors = []
    color_map = {'C':'Colorless'}
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
    for check_type in types.split(' '):
        if check_type in ['Artifact', 'Creature']:
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
for line in lines:
    if line == '' or line.startswith('#'):
        continue
    card_name, card_type, card_colors, card_sets, card_qty = line.split(';')
    card_qty = int(card_qty)
    card_colors = validate_colors(card_colors)
    card_type, card_subtype = validate_types(card_type)
    card_sets, card_rarities, card_formats, card_max = parse_sets(card_name, card_sets, restrictions.get(card_name))

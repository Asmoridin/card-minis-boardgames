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

raw_list = [] # Will hold the full list of cards

class Deck:
    """
    Helper class for a deck, keeping a track of the name and composition
    """
    def __init__(self, deck_name, deck_cards):
        """
        Basic constructor
        """
        self.deck_name = deck_name
        self.deck_cards = deck_cards

def read_decks(deck_format):
    """
    Takes in a format, and returns a list of Deck objects
    """
    ret_list = []
    if deck_format == 'Commander':
        for comm_color in os.listdir(DECK_DIR + '/' + deck_format):
            for deck_file in os.listdir(DECK_DIR + '/' + deck_format + "/" + comm_color):
                deck_name = deck_file.replace('.txt', '')
                this_deck = {}
                deck_fh = open(DECK_DIR + '/' + deck_format + '/' + comm_color + "/" + \
                        deck_file, 'r', encoding='UTF-8')
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
                ret_list.append(Deck(deck_name, this_deck))
    elif deck_format in os.listdir(DECK_DIR):
        for deck_file in os.listdir(DECK_DIR + '/' + deck_format):
            deck_name = deck_file.replace('.txt', '')
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
            ret_list.append(Deck(deck_name, this_deck))
    return ret_list

def check_decks(list_of_decks, list_of_cards):
    """
    Given:
    - a list of deck objects, and a list of relevant card tuples
    Return:
    - a list of tuples that are [DECK_NAME], [MISSING_NO], [MISSING_CARDS]
    """
    ret_list = []
    # First, construct a dict of the cards in the format
    inventory_dict = {}
    for in_card in list_of_cards:
        inventory_dict[in_card[0]] = in_card[7]
        #Potential card name cleanup
        cleanup_rules = {'û':'u', 'ó':'o'}
        clean_name = in_card[0]
        for start_letter, change_letter in cleanup_rules.items():
            clean_name = clean_name.replace(start_letter, change_letter)
        inventory_dict[clean_name] = in_card[7]
    for deck in list_of_decks:
        this_deck_missing = 0
        this_deck_missing_cards = {}
        for this_card, card_count in deck.deck_cards.items():
            if this_card in inventory_dict:
                if card_count > inventory_dict[this_card]:
                    this_deck_missing += card_count - inventory_dict[this_card]
                    this_deck_missing_cards[this_card] = card_count - inventory_dict[this_card]
            else:
                print(f"Missing card {this_card}")
                this_deck_missing += card_count
                this_deck_missing_cards[this_card] = card_count
        ret_list.append((deck.deck_name, this_deck_missing, this_deck_missing_cards))
    return ret_list

def aggregate_most_needed(deck_lists):
    """
    From a list of dicts, of cards missing for decks, generate a list of tuples of those cards
    and a total weight of said cards
    """
    ret_list = []
    temp_dict = {}
    for deck_list in deck_lists:
        for deck_card, deck_card_qty in deck_list[2].items():
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
                    'Standard', 'Pioneer', 'Oathbreaker', 'Ice Age Block', 'Mirage Block']:
                print("Unknown format: " + this_format)
            if bnr not in ['Banned', 'Restricted']:
                print("Unknown status: " + bnr)
            return_dict[this_card_name][this_format] = bnr
    return return_dict

    #Ixalan block (Ixalan, Rivals of Ixalan)
    #Amonkhet block (Amonkhet, Hour of Devastation)
    #Kaladesh block (Kaladesh, Aether Revolt)
    #Shadows over Innistrad block (Shadows over Innistrad, Eldritch Moon)
    #Battle for Zendikar block (Battle for Zendikar, Oath of the Gatewatch)
    #Khans of Tarkir block (Khans of Tarkir, Fate Reforged, Dragons of Tarkir)
    #Theros block (Theros, Born of the Gods, Journey into Nyx)
    #Return to Ravnica block (Return to Ravnica, Gatecrash, Dragon's Maze)
    #Innistrad block (Innistrad, Dark Ascension, Avacyn Restored)
    #Scars of Mirrodin block (Scars of Mirrodin, Mirrodin Besieged, New Phyrexia)
    #Zendikar block (Zendikar, Worldwake, Rise of the Eldrazi)
    #Alara block (Shards of Alara, Conflux, Alara Reborn)
    #Lorwyn–Shadowmoor block (Lorwyn, Morningtide, Shadowmoor, Eventide)
    #Time Spiral block (Time Spiral, Planar Chaos, Future Sight)
    #Ravnica block (Ravnica: City of Guilds, Guildpact, Dissension)
    #Kamigawa block (Champions of Kamigawa, Betrayers of Kamigawa, Saviors of Kamigawa)
    #Mirrodin block (Mirrodin, Darksteel, Fifth Dawn)
    #Onslaught block (Onslaught, Legions, Scourge)
    #Odyssey block (Odyssey, Torment, Judgment)
    #Invasion block (Invasion, Planeshift, Apocalypse)
    #Masques block (Mercadian Masques, Nemesis, Prophecy)
    #Urza's block (Urza's Saga, Urza's Legacy, Urza's Destiny)
    #Tempest block (Tempest, Stronghold, Exodus)

def parse_sets(this_card_name, card_set_string, card_restrictions):
    """
    The heavy lifting function of this module, where I go through and figure out rarites, sets,
    formats, and anything else
    """
    ret_sets = []
    ret_rarities = set()
    ret_formats = {"Commander": 1, "Vintage": 4, "Legacy": 4, "Oathbreaker":1}
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
            # Handle Ice Age Block
            if this_set in ['Ice Age', 'Coldsnap', 'Alliances']:
                ret_formats['Ice Age Block'] = 4
            # Handle Mirage Block
            if this_set in ['Mirage', 'Visions', 'Weatherlight']:
                ret_formats['Mirage Block'] = 4
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
    if types == 'Basic Snow Land':
        ret_type.append('Basic Land')
        ret_type.append('Snow')
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
        if check_type != '':
            ret_subtype.append(check_type)
    return(ret_type, ret_subtype)

def process_formats(format_name):
    """
    Given a format_name, process everything we need- find the suggested card, give stats on 
    the format, and parse, and sort the various decks.
    """
    return_dict = {}
    return_dict['FILTERED'] = {}
    format_card_list = []
    format_own = 0
    format_total = 0
    for in_card in raw_list:
        if format_name in in_card[6]:
            format_card_list.append(in_card)
            format_total += in_card[6][format_name]
            format_own += min(in_card[7], in_card[6][format_name])
    format_cards = len(format_card_list)
    FORMAT_LIST.append((format_name, format_own, format_total))

    return_dict['FILTERED']['set'], ft_filtered_list = sort_and_filter(format_card_list, 4)
    return_dict['FILTERED']['type'], ft_filtered_list = sort_and_filter(ft_filtered_list, 1)
    if return_dict['FILTERED']['type'] in ['Creature', 'Planeswalker']:
        _, ft_filtered_list = sort_and_filter(ft_filtered_list, 2)
    _, ft_filtered_list = sort_and_filter(ft_filtered_list, 3)
    _, ft_filtered_list = sort_and_filter(ft_filtered_list, 5)
    return_dict['FILTERED']['name'], ft_filtered_list = sort_and_filter(ft_filtered_list, 0)
    return_dict['ITEM'] = ft_filtered_list[0]

    format_decks = read_decks(format_name)
    format_decks_minus_own = check_decks(format_decks, format_card_list)
    format_most_needed = aggregate_most_needed(format_decks_minus_own)
    format_most_needed = sorted(format_most_needed, key=lambda x:(-1 * x[1], x[0]))
    format_decks_minus_own = sorted(format_decks_minus_own, key=lambda x:x[1])
    return_dict['FORMAT_OWN'] = format_own
    return_dict['FORMAT_TOTAL'] = format_total
    return_dict['FORMAT_CARDS'] = format_cards
    return_dict['DECKS'] = format_decks_minus_own
    return_dict['NEEDED'] = format_most_needed
    return return_dict

def handle_output(format_name, format_dict, dest_fh):
    """
    Handle the output, so I don't have to do this multiple times
    """
    double_print(f"\n*** {format_name.upper()} ***", dest_fh)

    tot_str = f"There are {format_dict['FORMAT_CARDS']} {format_name} legal cards"
    double_print(tot_str, dest_fh)

    summ_str = f"Have {format_dict['FORMAT_OWN']} out of {format_dict['FORMAT_TOTAL']} - " + \
        f"{100* format_dict['FORMAT_OWN']/format_dict['FORMAT_TOTAL']:.2f} percent of a playset"
    double_print(summ_str, dest_fh)

    purch_str = f"Chosen card is a(n) {format_dict['FILTERED']['type']} from " + \
        f"{format_dict['FILTERED']['set']} - {format_dict['FILTERED']['name']}. I own " + \
        f"{format_dict['ITEM'][7]} of {format_dict['ITEM'][6]['Legacy']}"
    double_print(purch_str, dest_fh)

    double_print(f"\nClosest deck to completion ({format_dict['DECKS'][0][0]}) is at " + \
        f"{format_dict['DECKS'][0][1]} cards.", dest_fh)
    double_print(str(format_dict['DECKS'][0][2]), dest_fh)

    double_print("\nMost needed cards are:", dest_fh)
    for pr_card_tuple in format_dict['NEEDED'][:10]:
        double_print(f" - {pr_card_tuple[0]}: {pr_card_tuple[1]}", dest_fh)

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

restrictions = parse_restrictions(restr_file_h.readlines())
restr_file_h.close()

SET_CHECK = 0
CHECK_SET = "Weatherlight"
CHECK_AMOUNT = 167
SET_CHECK += 10 # Extra basic lands

TOTAL_OWN = 0
TOTAL_MAX = 0
card_names = set()
creature_types = {}

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
    if CHECK_SET in card_sets:
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

for card in raw_list:
    if 'Vintage' not in card[6]:
        print("No Vintage?")
        print(card)

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
    vintage_dict = process_formats("Vintage")
    handle_output("Vintage", vintage_dict, out_file_h)

    # Legacy
    legacy_dict = process_formats("Legacy")
    handle_output("Legacy", legacy_dict, out_file_h)

    # Commander
    comm_dict = process_formats("Commander")
    handle_output("Commander", comm_dict, out_file_h)

    # Modern
    modern_dict = process_formats("Modern")
    handle_output("Modern", modern_dict, out_file_h)

    # Pioneer
    pioneer_dict = process_formats("Pioneer")
    handle_output("Pioneer", pioneer_dict, out_file_h)

    # Standard
    standard_dict = process_formats("Standard")
    handle_output("Standard", standard_dict, out_file_h)

    # Pauper
    pauper_dict = process_formats("Pauper")
    handle_output("Pauper", pauper_dict, out_file_h)

    # Oathbreaker
    oath_dict = process_formats("Oathbreaker")
    handle_output("Oathbreaker", oath_dict, out_file_h)

    # Ice Age Block
    ia_dict = process_formats("Ice Age Block")
    handle_output("Ice Age Block", ia_dict, out_file_h)

    # Mirage Block
    mir_dict = process_formats("Mirage Block")
    handle_output("Mirage Block", mir_dict, out_file_h)

    # Other
    double_print("\n*** OTHER DATA ***", out_file_h)
    double_print("Most common creature types:", out_file_h)
    USED_TYPES = ['Wall', 'Necron', 'Human', 'Cleric', 'Goblin', 'Squirrel',]
    for del_type in USED_TYPES:
        del creature_types[del_type]
    creature_types = sorted(creature_types.items(), key=lambda x:(-1 * x[1], x[0]))
    for creature_tuple in creature_types[:100]:
        double_print(f"- {creature_tuple[0]}: {creature_tuple[1]}", out_file_h)
    double_print("If above is 3, we should do a tribal Commander deck", out_file_h)

    double_print("\nPercentages ordered by format:", out_file_h)
    FORMAT_LIST = sorted(FORMAT_LIST, key=lambda x:(x[1]/x[2], x[0]), reverse=True)
    for print_format in FORMAT_LIST:
        double_print(f"{print_format[0]}: {100 * print_format[1]/print_format[2]:.2f}", out_file_h)

    print(f"Should be {CHECK_AMOUNT} for {CHECK_SET}: {SET_CHECK}")

    out_file_h.close()

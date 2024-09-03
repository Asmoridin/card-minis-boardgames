#!/usr/bin/python3

"""
Collection tracker/management for the DBS Fusion World card game
"""

import os
import sys

GAME_NAME = "Dragon Ball Super Card Game: Fusion World"

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

def read_decks(in_deck_lists):
    """
    Take in a list of deck list tuples, and return a list of deck objects
    """
    ret_list = []
    for in_deck in in_deck_lists:
        this_deck_name = in_deck[0]
        deck_dict = {}
        deck_contents_str = in_deck[1]
        deck_contents = deck_contents_str.split(',')
        for content_line in deck_contents:
            deck_card_no, deck_card_qty = content_line.split(':')
            deck_card_no = deck_card_no.replace('-F', '')
            deck_card_qty = int (deck_card_qty)
            if deck_card_no not in deck_dict:
                deck_dict[deck_card_no] = 0
            deck_dict[deck_card_no] += deck_card_qty
        ret_list.append(Deck(this_deck_name, deck_dict))
    return ret_list

def get_missing(in_decks, in_card_own_dict):
    """
    Takes in a list of decks, returns a list of decks with the cards I'm missing, with
    names attached
    """
    return_list = []
    for temp_deck in in_decks:
        missing_total = 0
        missing_cards = {}
        for check_card in temp_deck.deck_cards:
            if check_card not in in_card_own_dict:
                print("Card not found: " + check_card)
                continue
            if in_card_own_dict[check_card][1] < temp_deck.deck_cards[check_card]:
                missing_cards[in_card_own_dict[check_card][0]] = temp_deck.deck_cards[check_card] \
                    - in_card_own_dict[check_card][1]
                missing_total += missing_cards[in_card_own_dict[check_card][0]]
        return_list.append((temp_deck.deck_name, missing_total, missing_cards))
    return return_list

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/DBSCGFusionWorld.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'card_games/DB/Decks/DBSFusionWorld'
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/DBSCGFusionWorld.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'DB/Decks/DBSFusionWorld'
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

deck_lists = []
for file_name in os.listdir(DECK_DIR):
    dlh = open(DECK_DIR + "/" + file_name, 'r', encoding="UTF-8")
    deck_list = dlh.readlines()
    dlh.close()
    deck_list = [line.strip() for line in deck_list]
    for line in deck_list:
        if line.startswith('#'):
            continue
        line = line.replace('https://deckbuilder.egmanevents.com/?deck=', '')
        line = line.replace('&type=fusionworld', '')
        deck_lists.append((file_name, line))

sub_type_map = {}
TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
card_own_dict = {}
for line in lines:
    line = line.split('#')[0]
    try:
        card_name, card_subtypes, card_type, card_color, card_cost, card_number, card_set, \
            card_own = line.split(';')
    except ValueError:
        print("Failed on line:")
        print(line)
        continue
    try:
        card_own = int(card_own)
    except ValueError:
        print("Issue with number on line:")
        print(line)
        continue
    if card_subtypes == '':
        print("Missing subtypes:")
        print(line)
        continue
    card_subtypes = card_subtypes.split('/')
    for subtype in card_subtypes:
        if subtype not in sub_type_map:
            sub_type_map[subtype] = 0
        sub_type_map[subtype] += 1
    if card_type not in ['Leader', 'Battle', 'Extra']:
        print("Invalid card type: " + card_type)
        continue
    if card_color not in ['Green', 'Red', 'Blue', 'Yellow', 'Black',]:
        print("Invalid card color: " + card_color)
        continue
    CARD_MAX = 4
    if card_type == 'Leader':
        CARD_MAX = 1
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_subtypes, card_type, card_color, card_cost, card_number, \
        card_set, card_own, CARD_MAX))
    card_own_dict[card_number] = (f"{card_name} ({card_number})", card_own)

decks = read_decks(deck_lists)
get_deck_missing = get_missing(decks, card_own_dict)
get_deck_missing = sorted(get_deck_missing, key=lambda x:(x[1], x[0]))

# Filter by subtype
chosen_subtype, filtered_list = sort_and_filter(item_list, 1)

#Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 3)

# Filter by card type
chosen_type, filtered_list = sort_and_filter(filtered_list, 2)

# Filter by set
chosen_set, filtered_list = sort_and_filter(filtered_list, 6)

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
        out_file_h = open("card_games/output/DBSCGFusionWorld.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/DBSCGFusionWorld.txt", 'w', encoding="UTF-8")

    SUMMARY_STRING = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(SUMMARY_STRING, out_file_h)

    double_print(f"Want a {chosen_subtype}...", out_file_h)
    sugg_string = f"Buy {picked_item[0] + ' - ' + picked_item[5]} (" + \
        f"{picked_item[3] + ' ' + picked_item[2]}) from {picked_item[6]} (have " + \
        f"{picked_item[7]} out of {picked_item[8]})"
    double_print(sugg_string, out_file_h)

    double_print("\nLowest deck currently:", out_file_h)
    lowest_deck = get_deck_missing[0]
    double_print(f"{lowest_deck[0]} - Missing {lowest_deck[1]} cards", out_file_h)
    for print_name, print_qty in sorted(lowest_deck[2].items()):
        double_print(f"- {print_name}: {print_qty}", out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

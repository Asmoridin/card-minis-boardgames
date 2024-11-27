#!/usr/bin/python3

"""
Tool that provides the cards that are most commonly in decks that I don't own enough of.
"""

import os
import sys

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'card_games/Decks/StarWarsUnlimited'
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'Decks/StarWarsUnlimited'
    sys.path.append('.')
    from utils.output_utils import double_print

def parse_deck(deck_lines, collection_dict_in):
    """
    Take a list of lines from a deck that has een read in, and convert the lines
    into an output dictionary
    """
    ret_dict = {}
    for deck_line in deck_lines:
        deck_line = deck_line.strip()
        if deck_line.startswith('//') or deck_line == '':
            continue
        cards_needed, this_card_name = deck_line.split("\t")
        cards_needed = int(cards_needed)
        if this_card_name not in collection_dict_in:
            print("Unknown card: " + this_card_name)
        if this_card_name not in ret_dict:
            ret_dict[this_card_name] = cards_needed
        else:
            ret_dict[this_card_name] += cards_needed
    return ret_dict

def determine_missing(deck_dict, collection_dict_in):
    """
    Given a dictionary for a deck, return what cards I am missing
    """
    ret_dict = {}
    for card, deck_card_qty in deck_dict.items():
        if collection_dict_in[card] < deck_card_qty:
            ret_dict[card] = deck_card_qty - collection_dict_in[card]
    return ret_dict

collection_dict = {}
full_collection = {}
card_need_dict = {}
in_lines = file_h.readlines()
file_h.close()
for line in in_lines:
    if line.strip() == "" or line.startswith('#'):
        continue
    line = line.split('#')[0].strip()
    card_name = line.split(';')[0]
    card_own = int(line.split(';')[-1])
    collection_dict[card_name] = card_own
    full_collection[card_name] = 3
    if line.split(';')[2] in ['Base', 'Leader']:
        full_collection[card_name] = 1

for file_name in os.listdir(DECK_DIR):
    this_deck_file = DECK_DIR + "/" + file_name
    deck_file_h = open(this_deck_file, 'r', encoding="UTF-8")
    this_deck_lines = deck_file_h.readlines()
    deck_file_h.close()
    this_deck_dict = parse_deck(this_deck_lines, collection_dict)
    missing_cards = determine_missing(this_deck_dict, collection_dict)
    for missing_card, missing_card_qty in missing_cards.items():
        if missing_card not in card_need_dict:
            card_need_dict[missing_card] = 0
        card_need_dict[missing_card] += missing_card_qty

missing_full_cards = determine_missing(full_collection, collection_dict)
for missing_card, missing_card_qty in missing_full_cards.items():
    if missing_card not in card_need_dict:
        card_need_dict[missing_card] = 0
    card_need_dict[missing_card] += missing_card_qty

card_sorter = []
for card_name, card_qty in card_need_dict.items():
    card_sorter.append((card_name, card_qty))
card_sorter = sorted(card_sorter, key=lambda x:(-1 * x[1], x[0]))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/StarWarsUnlimitedDeckData.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/StarWarsUnlimitedDeckData.txt", 'w', encoding="UTF-8")

    for card_tuple in card_sorter:
        double_print(f"{card_tuple[0]}: {card_tuple[1]}", out_file_h)
    out_file_h.close()

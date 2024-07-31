#!/usr/bin/python3

"""
Tool to give me some deck information, based off the current meta
"""

import os
import sys

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/OnePieceData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'card_games/DB/Decks/OnePieceTCG'
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/OnePieceData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'DB/Decks/OnePieceTCG'
    sys.path.append('.')
    from utils.output_utils import double_print

def parse_deck(deck_lines, collection_dict_in):
    """
    Take a list of lines from a deck that has been read in, and convert the lines
    into an output dictionary
    """
    ret_dict = {}
    for deck_line in deck_lines:
        deck_line = deck_line.strip()
        if deck_line.startswith('#') or deck_line == '':
            continue
        cards_needed, this_card_number = deck_line.split("x")
        cards_needed = int(cards_needed)
        if this_card_number not in collection_dict_in:
            print("Unknown card: " + this_card_number)
        if this_card_number not in ret_dict:
            ret_dict[this_card_number] = cards_needed
        else:
            ret_dict[this_card_number] += cards_needed
    return ret_dict

def determine_missing(deck_dict, collection_dict_in):
    """
    Given a dictionary for a deck, return what cards I am missing
    """
    ret_dict = {}
    for this_card, deck_card_qty in deck_dict.items():
        if collection_dict_in[this_card] < deck_card_qty:
            ret_dict[this_card] = deck_card_qty - collection_dict_in[this_card]
    return ret_dict

collection_dict = {}
full_collection = {}
card_number_to_name_dict = {}
card_need_dict = {}
leaders = {}
in_lines = file_h.readlines()
file_h.close()
for line in in_lines:
    if line.strip() == "" or line.startswith('#'):
        continue
    line = line.split('#')[0].strip()
    card_name = line.split(';')[0]
    card_number = line.split(';')[1]
    card_own = int(line.split(';')[-1])
    if line.split(';')[2] == 'Leader':
        leaders[card_number] = (card_name, line.split(';')[3])
    collection_dict[card_number] = card_own
    card_number_to_name_dict[card_number] = card_name
    full_collection[card_number] = 4
    if line.split(';')[2] in ['Leader']:
        full_collection[card_number] = 1

deck_tuples = [] # (DeckFile, cards_needed, cards)
for file_name in os.listdir(DECK_DIR):
    CARDS_NEEDED = 0
    this_deck_file = DECK_DIR + "/" + file_name
    deck_file_h = open(this_deck_file, 'r', encoding="UTF-8")
    this_deck_lines = deck_file_h.readlines()
    deck_file_h.close()
    this_deck_dict = parse_deck(this_deck_lines, collection_dict)
    for card_num, _ in this_deck_dict.items():
        if card_num in leaders:
            del leaders[card_num]
    missing_cards = determine_missing(this_deck_dict, collection_dict)
    for card, card_qty in missing_cards.items():
        CARDS_NEEDED += card_qty
    deck_tuples.append((file_name, CARDS_NEEDED, missing_cards))
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
for card_number, card_qty in card_need_dict.items():
    card_name = card_number_to_name_dict[card_number]
    card_sorter.append((card_name, card_number, card_qty))
card_sorter = sorted(card_sorter, key=lambda x:(-1 * x[2], x[0], x[1]))

deck_sorter = []
deck_sorter = sorted(deck_tuples, key=lambda x:x[1])

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/OnePieceDeckData.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/OnePieceDeckData.txt", 'w', encoding="UTF-8")

    for card_tuple in card_sorter:
        double_print(f"{card_tuple[0]} ({card_tuple[1]}): {card_tuple[2]}", out_file_h)

    if len(leaders) > 0:
        double_print("Missing leaders: ", out_file_h)
        for card_number, card_tuple in sorted(leaders.items(), key=lambda x:(x[1][0], x[0])):
            double_print(f"- {card_tuple[0]} ({card_tuple[1]}), ({card_number})", out_file_h)

    double_print("\nLowest deck: ", out_file_h)
    double_print(f"Deck File: {deck_sorter[0][0]}, needing {deck_sorter[0][1]} cards", out_file_h)
    missing_lowest_deck_cards = deck_sorter[0][2]
    print(missing_lowest_deck_cards)
    out_file_h.close()

#!/usr/bin/python3

import sys, os

GAME_NAME = "Star Trek: Second Edition"

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/StarTrek2EData.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/StarTrek2EData.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

total_max = 0
total_own = 0
card_names = set()
card_lines = []
filter_lines = []
for line in lines:
    if line == '':
        continue

    line = line.split('//')[0].strip()
    card_name, rarity, card_type, card_affil, card_set, print_type, max_card, card_own = line.split(';')
    if card_name in card_names:
        print("Duplicate card name: " + card_name)
    card_names.add(card_name)
    rarity = rarity.split('/')
    for in_rarity in rarity:
        if in_rarity not in ['C', 'U', 'R', 'S', 'P', 'VP', 'V', 'B']:
            print("Invalid rarity of %s for %s" % (in_rarity, card_name))
    if card_type not in ['Personnel', 'Ship', 'Dilemma', 'Equipment', 'Event', 'Interrupt', 'Mission', ]:
        print("Invalid card type of %s for %s" % (card_type, card_name))
    if print_type not in ['Print', 'Virtual', 'Both']:
        print("Invalid print type of %s for %s" % (print_type, card_name))
    max_card = int(max_card)
    card_own = int(card_own)
    total_max += max_card
    total_own += card_own
    filter_lines.append((print_type, card_set, card_type, card_affil, rarity, card_name, max_card, card_own))

print_type_map = {}
# Filter by print type
for line in filter_lines:
    print_type = line[0]
    if print_type not in print_type_map:
        print_type_map[print_type] = [0, 0]
    print_type_map[print_type][0] += line[6]
    print_type_map[print_type][1] += line[7]
print(print_type_map)
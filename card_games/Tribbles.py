#!/usr/bin/python3

import sys, os

GAME_NAME = "Tribbles"

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/TribblesData.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/TribblesData.txt', 'r')
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
    line = line.split('//')[0].strip()
    card_name, card_type, card_sets, max_item, own_item = line.split(';')
    if card_name in card_names:
        print("Duplicate: " + card_name)
    card_names.add(card_name)
    max_item = int(max_item)
    own_item = int(own_item)
    if card_type == 'Tribble':
        card_count, card_power = card_name.split('-')
        card_count = card_count.strip()
        card_power = card_power.strip()
        card_lines.append((card_count, card_power, max_item, own_item))
    elif card_type == 'Trouble':
        pass
    total_max += max_item
    total_own += own_item

# Figure out appropriate Tribble power
card_power_map = {}
for line in card_lines:
    if line[1] not in card_power_map:
        card_power_map[line[1]] = [0, 0]
    card_power_map[line[1]][0] += line[2]
    card_power_map[line[1]][1] += line[3]
card_power_sorter = []
for card_power in card_power_map:
    card_power_sorter.append((card_power, card_power_map[card_power][1]/card_power_map[card_power][0], card_power_map[card_power][0] - card_power_map[card_power][1]))
card_power_sorter = sorted(card_power_sorter, key=lambda x:(x[1], -x[2], x[0]))

# Filter out by power, then sort by quantity
card_qty_map = {}
for line in card_lines:
    if line[1] == card_power_sorter[0][0]:
        if line[0] not in card_qty_map:
            card_qty_map[line[0]] = [0, 0]
        card_qty_map[line[0]][0] += line[2]
        card_qty_map[line[0]][1] += line[3]
card_qty_sorter = []
for card_qty in card_qty_map:
    card_qty_sorter.append((card_qty, card_qty_map[card_qty][1]/card_qty_map[card_qty][0], card_qty_map[card_qty][0] - card_qty_map[card_qty][1]))
card_qty_sorter = sorted(card_qty_sorter, key=lambda x:(x[1], -x[2], x[0]))
print(card_qty_sorter)
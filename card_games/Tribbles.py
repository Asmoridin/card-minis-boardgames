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
    max_item = int(max_item)
    own_item = int(own_item)
    card_lines.append((card_name, card_type, card_sets, max_item, own_item))
    total_max += max_item
    total_own += own_item

card_type_map = {}
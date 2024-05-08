#!/usr/bin/python3

import sys, os

GAME_NAME = "Star Trek: Second Edition"

physical_sets = ['Necessary Evil', 'Energize', 'What You Leave Behind', 'Second Edition', 'Call to Arms', 'Tenth Anniversary Collection', 'Fractured Time'
    'Reflections 2.0', 'Archive Portrait', 'Strange New Worlds', 'To Boldly Go', 'Dangerous Missions', "Captain's Log", 'Genesis', 'These Are The Voyages',
    'In A Mirror Darkly', 'What You Leave Behind', ]

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/StarTrek2EData.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('DB/StarTrek2EData.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
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
        if in_rarity not in ['C', 'U', 'R', 'S', 'P', 'VP', 'V', 'B', 'AP', ]:
            print("Invalid rarity of %s for %s" % (in_rarity, card_name))
    if card_type not in ['Personnel', 'Ship', 'Dilemma', 'Equipment', 'Event', 'Interrupt', 'Mission', ]:
        print("Invalid card type of %s for %s" % (card_type, card_name))
    if print_type not in ['Print', 'Virtual', 'Both']:
        print("Invalid print type of %s for %s" % (print_type, card_name))
    card_set = card_set.split('/')
    max_card = int(max_card)
    card_own = int(card_own)
    TOTAL_MAX += max_card
    TOTAL_OWN += card_own
    filter_lines.append((print_type, card_set, card_type, card_affil, rarity, card_name, card_own, max_card))

print_type_map = {'Print':[0,0], 'Virtual':[0,0]}
# Sort by print type
for line in filter_lines:
    print_type = line[0]
    if print_type in ['Print', 'Virtual']:
        print_type_map[print_type][0] += line[7]
        print_type_map[print_type][1] += line[6]
    if print_type == 'Both':
        print_type_map['Print'][0] += line[7]
        print_type_map['Print'][1] += line[6]
        print_type_map['Virtual'][0] += line[7]
        print_type_map['Virtual'][1] += line[6]
print_type_sorter = []
for print_type in print_type_map:
    print_type_sorter.append((print_type, print_type_map[print_type][1]/print_type_map[print_type][0], print_type_map[print_type][0] - print_type_map[print_type][1]))
print_type_sorter = sorted(print_type_sorter, key=lambda x:(x[1], -x[2], x[0]))

new_filter_lines = []
for line in filter_lines:
    if line[0] == print_type_sorter[0][0] or line[0] == 'Both':
        new_filter_lines.append(line)
filter_lines = new_filter_lines

# Sort/filter by card set
chosen_set, filtered_lines = sort_and_filter(filter_lines, 1)

# Sort by card type, and filter by card set
chosen_card_type, filtered_lines = sort_and_filter(filtered_lines, 2)

# For certain type, sort/filter by affiliation
if chosen_card_type == 'Ship' or chosen_card_type == 'Personnel':
    chosen_affil, filtered_lines = sort_and_filter(filtered_lines, 3)
    #print(chosen_affil)

# Find a final card to go with
chosen_card, filtered_lines = sort_and_filter(filtered_lines, 5)
final_card = filtered_lines[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/ST2EOut.txt", 'w')
    else:
        out_file_h = open("output/ST2EOut.txt", 'w')
    
    double_print("Have %d out of %d - %.2f percent" % (TOTAL_OWN, TOTAL_MAX, TOTAL_OWN * 100/TOTAL_MAX), out_file_h)
    double_print("Buy a %s from %s, maybe %s (have %d out of %d)" % (final_card[2], chosen_set, final_card[5], final_card[7], final_card[6]), out_file_h)

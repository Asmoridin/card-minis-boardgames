#!/usr/bin/python3

"""
Tracker and army suggestion tool for games of Star Wars: Unlimited
"""

import os
import sys
sys.path.append('.')
from utils.output_utils import double_print


if os.getcwd().endswith('card-minis-boardgames'):
    out_file_h = open("win_loss/output/SWUnlimitedOut.txt", 'w', encoding="UTF-8")
    in_file = open('win_loss/DB/SWUnlimited-Results.txt', 'r', encoding="UTF-8")
    source_data_file = open('card_games/DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("output/SWUnlimitedOut.txt", 'w', encoding="UTF-8")
    in_file = open('DB/SWUnlimited-Results.txt', 'r', encoding="UTF-8")
    source_data_file = open('../card_games/DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")

double_print("Star Wars: Unlimited W/L Loss Tracker, and deck selector", out_file_h)

aspect_map = {'R':'Aggression', 'Y':'Cunning', 'U':'Vigilance', 'G':'Command', 'B':'Villainy', 'W':'Heroism'}
base_aspects = ['Aggression', 'Cunning', 'Vigilance', 'Command']

data_lines = in_file.readlines()
in_file.close()
data_lines = [line.strip() for line in data_lines]

source_data_lines = source_data_file.readlines()
source_data_file.close()
source_data_lines = [line.strip() for line in source_data_lines]
valid_leaders = {}
leader_games_map = {} # Total number of games I've seen the leader
for line in source_data_lines:
    if line.split(';')[2] == 'Leader':
        leader_name = line.split(';')[0]
        aspects = []
        for aspect in line.split(';')[3].split('/'):
            aspects.append(aspect_map[aspect])
        valid_leaders[leader_name] = aspects
        leader_games_map[leader_name] = 0

my_leader_wl = {}
my_opp_wl = {}
my_opp_leader_wl = {}
total_wl = [0, 0]
my_aspect_wl = {}

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    my_leader, base_aspect, opponent, opp_leader, opp_base_aspect, w_l = line.split(';')

    if my_leader not in valid_leaders:
        double_print(f"Invalid leader: {my_leader}", out_file_h)
    if opp_leader not in valid_leaders:
        double_print(f"Invalid leader: {opp_leader}", out_file_h)

    base_aspect = aspect_map[base_aspect]
    opp_base_aspect = aspect_map[opp_base_aspect]
    my_aspects = [base_aspect]
    my_aspects.extend(valid_leaders[my_leader])
    my_aspects = sorted(list(set(my_aspects)))
    for aspect in my_aspects:
        if aspect not in my_aspect_wl:
            my_aspect_wl[aspect] = [0, 0]

    leader_games_map[my_leader] += 1
    leader_games_map[opp_leader] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if my_leader not in my_leader_wl:
        my_leader_wl[my_leader] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if opp_leader not in my_opp_leader_wl:
        my_opp_leader_wl[opp_leader] = [0, 0]

    if w_l == 'W':
        my_leader_wl[my_leader][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_leader_wl[opp_leader][0] += 1
        for aspect in my_aspects:
            my_aspect_wl[aspect][0] += 1
    if w_l == 'L':
        my_leader_wl[my_leader][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_leader_wl[opp_leader][1] += 1
        for aspect in my_aspects:
            my_aspect_wl[aspect][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print("My record by leader:", out_file_h)
for leader in sorted(my_leader_wl):
    double_print(f"{leader}: {my_leader_wl[leader][0]}-{my_leader_wl[leader][1]}", out_file_h)

leader_h_index = []
for leader, l_w_l in my_leader_wl.items():
    leader_h_index.append((leader, sum(l_w_l)))
leader_h_index = sorted(leader_h_index, key=lambda x:x[1], reverse=True)
H_INDEX = 0
for x, leader in enumerate(leader_h_index):
    H_INDEX += 1
    if not leader[1] >= H_INDEX:
        H_INDEX = H_INDEX - 1
        break
double_print(f"\nMy H-Index is {H_INDEX}", out_file_h)

double_print("\nMy record by aspect:", out_file_h)
for aspect in sorted(my_aspect_wl):
    double_print(f"{aspect}: {my_aspect_wl[aspect][0]}-{my_aspect_wl[aspect][1]}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing leaders:", out_file_h)
for opp_leader in sorted(my_opp_leader_wl):
    double_print(f"{opp_leader}: {my_opp_leader_wl[opp_leader][0]}-{my_opp_leader_wl[opp_leader][1]}", out_file_h)

MIN_SEEN = 1000000
min_seen_leaders = []
for leader in leader_games_map:
    if leader_games_map[leader] < MIN_SEEN:
        MIN_SEEN = leader_games_map[leader]
        min_seen_leaders = [leader]
    elif leader_games_map[leader] == MIN_SEEN:
        min_seen_leaders.append(leader)
double_print(f"\nI've seen these leaders on the table the least ({MIN_SEEN} times): {'; '.join(sorted(min_seen_leaders))}", out_file_h)

playable_leader_list = []
for leader in valid_leaders:
    if leader not in my_leader_wl:
        playable_leader_list.append((leader, 0))
    else:
        playable_leader_list.append((leader, sum(my_leader_wl[leader])))
playable_army_list = sorted(playable_leader_list, key=lambda x:(x[1], x[0]))
least_leader = playable_leader_list[0][0]
least_leader_games = playable_leader_list[0][1]

double_print(f"\nI should play more games with {least_leader}, as I only have {least_leader_games} game{('', 's')[least_leader_games != 1]}", out_file_h)
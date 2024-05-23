#!/usr/bin/python3

"""
Tracker and army suggestion tool for games of Manoeuvre
"""

import os
import sys

armies = ['Austria', 'France', 'Great Britain', 'Ottoman', 'Prussia', 'Russia', 'Spain',
          'United States', 'Sweden', 'India', 'China', 'Japan']

army_games_map = {}
for army in armies:
    army_games_map[army] = 0

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('win_loss/DB/ManoData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/ManoData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print

data_lines = file_h.readlines()
file_h.close()
data_lines = [line.strip() for line in data_lines]

if os.getcwd().endswith('card-minis-boardgames'):
    out_file_h = open("win_loss/output/ManoOut.txt", 'w', encoding="UTF-8")
else:
    out_file_h = open("output/ManoOut.txt", 'w', encoding="UTF-8")

my_army_wl = {}
my_opp_wl = {}
my_opp_army_wl = {}
total_wl = [0, 0]

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    MY_ARMY, OPP_ARMY, opponent, w_l, vic_type = line.split(';')
    if MY_ARMY == "GB":
        MY_ARMY = "Great Britain"
    if OPP_ARMY == "GB":
        OPP_ARMY = "Great Britain"
    if MY_ARMY == "US":
        MY_ARMY = "United States"
    if OPP_ARMY == "US":
        OPP_ARMY = "United States"
    if MY_ARMY not in armies:
        double_print(f"Invalid army: {MY_ARMY}", out_file_h)
    if OPP_ARMY not in armies:
        double_print(f"Invalid army: {OPP_ARMY}", out_file_h)
    army_games_map[MY_ARMY] += 1
    army_games_map[OPP_ARMY] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if vic_type not in ['Cas', 'NF']:
        double_print(f"Invalid victory type: {vic_type}", out_file_h)

    if MY_ARMY not in my_army_wl:
        my_army_wl[MY_ARMY] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if OPP_ARMY not in my_opp_army_wl:
        my_opp_army_wl[OPP_ARMY] = [0, 0]

    if w_l == 'W':
        my_army_wl[MY_ARMY][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_army_wl[OPP_ARMY][0] += 1
    if w_l == 'L':
        my_army_wl[MY_ARMY][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_army_wl[OPP_ARMY][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print("My record by army:", out_file_h)
for army in sorted(my_army_wl):
    double_print(f"{army}: {my_army_wl[army][0]}-{my_army_wl[army][1]}", out_file_h)

army_h_index = []
for army, a_w_l in my_army_wl.items():
    army_h_index.append((army, sum(a_w_l)))
army_h_index = sorted(army_h_index, key=lambda x:x[1], reverse=True)
H_INDEX = 0
for x in range(0, len(army_h_index)):
    H_INDEX += 1
    if not army_h_index[x][1] >= H_INDEX:
        H_INDEX = H_INDEX - 1
        break
double_print(f"\nMy H-Index is {H_INDEX}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing armies:", out_file_h)
for opp_army in sorted(my_opp_army_wl):
    opp_army_string = f"{opp_army}: {my_opp_army_wl[opp_army][0]}-{my_opp_army_wl[opp_army][1]}"
    double_print(opp_army_string, out_file_h)

MIN_SEEN = 1000000
min_seen_armies = []
for army in army_games_map:
    if army_games_map[army] < MIN_SEEN:
        MIN_SEEN = army_games_map[army]
        min_seen_armies = [army]
    elif army_games_map[army] == MIN_SEEN:
        min_seen_armies.append(army)
double_print(f"\nI've seen these armies on the table the least {MIN_SEEN} times: " + \
    f"{', '.join(sorted(min_seen_armies))}", out_file_h)

playable_army_list = []
for army in armies:
    if army not in my_army_wl:
        playable_army_list.append((army, 0))
    else:
        playable_army_list.append((army, sum(my_army_wl[army])))
playable_army_list = sorted(playable_army_list, key=lambda x:(x[1], x[0]))
least_army = playable_army_list[0][0]
least_army_games = playable_army_list[0][1]

double_print(f"\nI should play more games with {least_army}, as I only have {least_army_games} game{('', 's')[least_army_games != 1]}", out_file_h)

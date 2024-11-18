#!/usr/bin/python3

"""
Tracker and army suggestion tool for Star Fleet Battles tournament games
"""

import os
import sys
sys.path.append('.')
from utils.output_utils import double_print
from utils.get_h_index import get_h_index

if os.getcwd().endswith('card-minis-boardgames'):
    out_file_h = open("win_loss/output/SFBOut.txt", 'w', encoding="UTF-8")
    in_file = open('win_loss/DB/SFBWL.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("output/SFBOut.txt", 'w', encoding="UTF-8")
    in_file = open('DB/SFBWL.txt', 'r', encoding="UTF-8")

all_ships = ['Federation TCC', 'Hydran TLM', 'Klingon D7CT', 'Wyn TAxBC', 'Gorn TCC', 'LDR TCWL',
    'Tholian TNCA', 'Orion TBR', 'ISC TCA', 'Romulan TFH', 'Romulan TKE', 'Seltorian TCA',
    'Romulan TKR', 'Lyran TCC', 'Wyn TCA', 'Kzinti TCC', 'Archeo-Tholian TCC'
]

double_print("Star Fleet Battles Win-Loss Tracker and ship selector", out_file_h)

data_lines = in_file.readlines()
in_file.close()
data_lines = [line.strip() for line in data_lines]

my_ship_wl = {}
my_opp_wl = {}
my_opp_ship_wl = {}
total_wl = [0, 0]
ship_games_map = {}
for ship in all_ships:
    ship_games_map[ship] = 0

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    my_ship, opp_ship, opponent, w_l = line.split(';')

    if my_ship not in all_ships:
        double_print(f"Invalid Ship: {my_ship}", out_file_h)
        continue
    if opp_ship not in all_ships:
        double_print(f"Invalid Ship: {opp_ship}", out_file_h)
        continue

    ship_games_map[my_ship] += 1
    ship_games_map[opp_ship] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if my_ship not in my_ship_wl:
        my_ship_wl[my_ship] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if opp_ship not in my_opp_ship_wl:
        my_opp_ship_wl[opp_ship] = [0, 0]

    if w_l == 'W':
        my_ship_wl[my_ship][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_ship_wl[opp_ship][0] += 1
    if w_l == 'L':
        my_ship_wl[my_ship][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_ship_wl[opp_ship][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print(f"My record by ship ({len(all_ships)} total ships):", out_file_h)
for ship in sorted(my_ship_wl):
    double_print(f"{ship}: {my_ship_wl[ship][0]}-{my_ship_wl[ship][1]}", out_file_h)

ship_h_index = []
for ship, l_w_l in my_ship_wl.items():
    ship_h_index.append((ship, sum(l_w_l)))
ship_h_index = sorted(ship_h_index, key=lambda x:x[1], reverse=True)

double_print(f"\nMy H-Index is {get_h_index(ship_h_index)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing ships:", out_file_h)
for opp_ship in sorted(my_opp_ship_wl):
    ship_str = f"{opp_ship}: {my_opp_ship_wl[opp_ship][0]}-{my_opp_ship_wl[opp_ship][1]}"
    double_print(ship_str, out_file_h)

MIN_SEEN = 1000000
min_seen_ships = []
for ship, ship_games in ship_games_map.items():
    if ship_games < MIN_SEEN:
        MIN_SEEN = ship_games
        min_seen_ships = [ship]
    elif ship_games == MIN_SEEN:
        min_seen_ships.append(ship)
double_print(f"\nI've seen these ships on the table the least ({MIN_SEEN} times): " + \
    f"{'; '.join(sorted(min_seen_ships))}", out_file_h)

playable_ship_list = []
for ship in all_ships:
    if ship not in my_ship_wl:
        playable_ship_list.append((ship, 0))
    else:
        playable_ship_list.append((ship, sum(my_ship_wl[ship])))
playable_ship_list = sorted(playable_ship_list, key=lambda x:(x[1], x[0]))
least_ship = playable_ship_list[0][0]
least_ship_games = playable_ship_list[0][1]

sugg_string = f"\nI should play more games with the {least_ship}, as I only have " + \
    f"{least_ship_games} game{('', 's')[least_ship_games != 1]}"
double_print(sugg_string, out_file_h)

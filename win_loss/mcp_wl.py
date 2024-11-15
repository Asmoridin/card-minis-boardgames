#!/usr/bin/python3

"""
Win-Loss Tracker and play suggester for Marvel: Crisis Protocol
"""

import os
import sys
sys.path.append('.')
from utils.output_utils import double_print
from utils.get_h_index import get_h_index
from minis_games import marvel_crisis_protocol

if os.getcwd().endswith('card-minis-boardgames'):
    out_file_h = open("win_loss/output/MCPWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('win_loss/DB/MCPResults.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("output/MCPWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('DB/MCPResults.txt', 'r', encoding="UTF-8")

double_print("Marvel: Crisis Protocol Win-Loss Tracker and army selector\n", out_file_h)

all_affil_leaders = marvel_crisis_protocol.leaders
my_affil_leaders = {}
for affil, affil_members in all_affil_leaders.items():
    for affil_member in affil_members:
        if affil_member in marvel_crisis_protocol.owned_models:
            if affil not in my_affil_leaders:
                my_affil_leaders[affil] = []
            my_affil_leaders[affil].append(affil_member)
# Handling affiliations with no actual leaders
my_affil_leaders['Convocation'] = []
my_affil_leaders['Weapon X'] = []

# Read in the play data.
game_lines = in_file.readlines()
in_file.close()
game_lines = [line.strip() for line in game_lines]
for game_line in game_lines:
    if game_line == "":
        continue
    my_faction, my_leader, opp_faction, opp_leader, result, opponent, extract, secure = \
        game_line.split(';')
    if my_faction not in all_affil_leaders:
        print(f"I played an unknown faction: {my_faction}")
        continue
    if opp_faction not in all_affil_leaders:
        print(f"Opponent played an unknown faction: {opp_faction}")
        continue
    LEADERLESS_FACTIONS = ['Weapon X', 'Convocation']
    if my_faction not in LEADERLESS_FACTIONS and my_leader not in all_affil_leaders[my_faction]:
        print(f"Unknown leader {my_leader} for faction {my_faction}")
        continue
    if opp_faction not in LEADERLESS_FACTIONS and opp_leader not in all_affil_leaders[opp_faction]:
        print(f"Unknown leader {opp_leader} for faction {opp_faction}")
        continue
    if result not in ['W', 'L']:
        print(f"Invalid result: {result}")
        continue
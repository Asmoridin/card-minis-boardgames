#!/usr/bin/python3

"""
Win-Loss tracker and ID suggestion tool for Android: Netrunner
"""

import os
import sys
sys.path.append('.')
from utils.output_utils import double_print

if os.getcwd().endswith('card-minis-boardgames'):
    out_file_h = open("win_loss/output/NetrunnerOut.txt", 'w', encoding="UTF-8")
    in_file = open('win_loss/DB/AndroidNetrunnerWL.txt', 'r', encoding="UTF-8")
    id_data_file = open('win_loss/DB/NetrunnerIDs.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("output/NetrunnerOut.txt", 'w', encoding="UTF-8")
    in_file = open('DB/AndroidNetrunnerWL.txt', 'r', encoding="UTF-8")
    id_data_file = open('DB/NetrunnerIDs', 'r', encoding="UTF-8")

double_print("Android: Netrunner W/L Loss Tracker, and deck selector", out_file_h)

CORP_FACTIONS = ['Weyland', 'Haas-Bioroid', 'NBN', 'Jinteki', 'Neutral Corp']
RUNNER_FACTIONS = ['Neutral Runner', 'Shaper', 'Anarch', 'Criminal']

# Let's read the IDs, and parse the ID data
identities = {'Startup':{}, 'Standard':{}, 'Extended':{}}
id_by_faction = {}
id_to_faction = {}
id_total_plays = {}
id_lines = id_data_file.readlines()
id_data_file.close()
id_lines = [line.strip() for line in id_lines]
for id_line in id_lines:
    identity_name, ID_FACTION, id_format = id_line.split(';')
    if ID_FACTION == 'HB':
        ID_FACTION = 'Haas-Bioroid'
    if ID_FACTION not in CORP_FACTIONS and ID_FACTION not in RUNNER_FACTIONS:
        print(f"Unknown faction {ID_FACTION} for ID {identity_name}")
        continue
    if id_format not in ['Standard', 'Extended', 'Startup']:
        print(f"Unknown format {id_format} for ID {identity_name}")
        continue
    if ID_FACTION not in id_by_faction:
        id_by_faction[ID_FACTION] = []
    id_by_faction[ID_FACTION].append(identity_name)
    id_to_faction[identity_name] = ID_FACTION
    id_total_plays[identity_name] = 0
    do_formats = ['Extended']
    if id_format == 'Standard' or id_format == 'Startup':
        do_formats.append('Standard')
    if id_format == 'Startup':
        do_formats.append('Startup')
    for do_format in do_formats:
        if ID_FACTION not in identities[do_format]:
            identities[do_format][ID_FACTION] = []
        identities[do_format][ID_FACTION].append(identity_name)

# Let's start parsing the W-L data
id_wl = {} # For each ID, the total win loss
faction_wl = {} # For each faction, it's win-loss
opp_wl = {} # Win-Loss by opponent
opp_faction_wl = {} # W-L against each faction
total_wl = [0, 0]
in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]
for line in in_lines:
    my_id, opp_id, opp_name, result = line.split(';')
    if my_id not in id_to_faction:
        print(f"My ID not recognized: {my_id}")
        continue
    if opp_id not in id_to_faction:
        print(f"Opponent's ID not recognized: {opp_id}")
        continue
    my_faction = id_to_faction[my_id]
    opp_faction = id_to_faction[opp_id]
    if result not in ['W', 'L']:
        print("Invalid response in line:")
        print(line)
        continue
    if my_id not in id_wl:
        id_wl[my_id] = [0, 0]
    if my_faction not in faction_wl:
        faction_wl[my_faction] = [0, 0]
    if opp_name not in opp_wl:
        opp_wl[opp_name] = [0, 0]
    if opp_faction not in opp_faction_wl:
        opp_faction_wl[opp_faction] = [0, 0]
    if result == 'W':
        total_wl[0] += 1
        id_wl[my_id][0] += 1
        faction_wl[my_faction][0] += 1
        opp_wl[opp_name][0] += 1
        opp_faction_wl[opp_faction][0] += 1
        id_total_plays[my_id] += 1
    if result == 'L':
        total_wl[1] += 1
        id_wl[my_id][1] += 1
        faction_wl[my_faction][1] += 1
        opp_wl[opp_name][1] += 1
        opp_faction_wl[opp_faction][1] += 1
        id_total_plays[my_id] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print("My record by identity:", out_file_h)
for faction, faction_ids in sorted(id_by_faction.items()):
    faction_wl_str = f"{faction}:"
    if faction in faction_wl:
        faction_wl_str = f"{faction} ({faction_wl[faction][0]}-{faction_wl[faction][1]}):"
    double_print(faction_wl_str, out_file_h)
    for id_name in faction_ids:
        if id_name in id_wl:
            double_print(f" - {id_name}: {id_wl[id_name][0]}-{id_wl[id_name][1]}", out_file_h)

double_print("\nMy record against various factions:", out_file_h)
for opp_faction, fac_wl in sorted(opp_faction_wl.items()):
    faction_wl_str = f"- {opp_faction}: {fac_wl[0]}-{fac_wl[1]}"
    double_print(faction_wl_str, out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent, this_opp_wl in sorted(opp_wl.items()):
    opp_wl_str = f"- {opponent}: {this_opp_wl[0]}-{this_opp_wl[1]}"
    double_print(opp_wl_str, out_file_h)

double_print("\nSuggestion?", out_file_h)

#!/usr/bin/python3

"""
Scenario searcher/information for Nations at War by LNL
"""

import os
import sys

valid_countries = ['Germany', 'USSR', 'UK', 'USA', 'France', 'Canada', 'Poland', 'Italy', 
    'Vichy France', ]
month_map = {1:'January', 2:'February',}

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('board_games/DB/NationsAtWarScens.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter
else:
    file_h = open('board_games/DB/NationsAtWarScens', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
    from utils.sort_and_filter import sort_and_filter

scenarios = []
for line in file_h.readlines():
    if line.startswith('#'):
        continue
    line = line.strip()
    scenario_name, in_axis_country, in_allied_country, scen_date, scen_location, scen_theater, \
        in_maps, turns, product = line.split(';')
    axis_countries = []
    allied_countries = []
    for country in in_axis_country.split(','):
        if country.strip() not in valid_countries:
            print("Invalid axis country: " + country.strip())
        else:
            axis_countries.append(country.strip())
    for country in in_allied_country.split(','):
        if country.strip() not in valid_countries:
            print("Invalid allied country: " + country.strip())
        else:
            allied_countries.append(country.strip())
    # VALIDATE DATE
    if scen_theater not in ['Western', 'Eastern', 'African', 'Mediterranean']:
        print("Invalid scenario theater: " + scen_theater)
    maps = []
    for in_map in in_maps.split(','):
        maps.append(int(in_map.strip()))
    if turns != 'Variable':
        turns = int(turns)
    if product not in ['Desert Heat', "Stalin's Triumph", 'White Star Rising', 'Compendium 1', ]:
        print("Invalid product: " + product)
    scenarios.append((scenario_name, axis_countries, allied_countries, scen_date, scen_location, scen_theater, \
        maps, turns, product))

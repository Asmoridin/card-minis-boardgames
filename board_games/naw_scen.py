#!/usr/bin/python3

"""
Scenario searcher/information for Nations at War by LNL
"""

import os
import sys

valid_countries = ['Germany', 'USSR', 'UK', 'USA', 'France', 'Canada', 'Poland', 'Italy',
    'Vichy France', ]
month_map = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July',
    8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('board_games/DB/NationsAtWarScens.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('board_games/DB/NationsAtWarScens', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print

scenarios = []
map_dict = {}
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
    scen_date = scen_date.split('/')
    scen_date = [int(date_item.strip()) for date_item in scen_date]
    if scen_date[0] not in month_map:
        print(f"Invalid month: {scen_date[0]}")
    if scen_date[1] < 1 or scen_date[1] > 31:
        print(f"Invalid date: {scen_date[1]}")
    if scen_date[2] < 1936 or scen_date[1] > 1945:
        print(f"Invalid year: {scen_date[2]}")
    if scen_theater not in ['Western', 'Eastern', 'African', 'Mediterranean']:
        print("Invalid scenario theater: " + scen_theater)
    maps = []
    for in_map in in_maps.split(','):
        maps.append(int(in_map.strip()))
    for used_map in maps:
        if used_map not in map_dict:
            map_dict[used_map] = 0
        map_dict[used_map] += 1
    if turns != 'Variable':
        turns = int(turns)
    if product not in ['Desert Heat', "Stalin's Triumph", 'White Star Rising', 'Compendium 1', ]:
        print("Invalid product: " + product)
    scenarios.append((scenario_name, axis_countries, allied_countries, scen_date, scen_location, \
        scen_theater, maps, turns, product))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("board_games/output/NAWScenarios.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/NAWScenarios.txt", 'w', encoding="UTF-8")

    double_print(f"There are {len(scenarios)} total scenarios.", out_file_h)

    map_sorted = sorted(map_dict.items(), key=lambda x:x[1], reverse=True)
    map_str = f"Out of {len(map_dict)} maps, map {map_sorted[0][0]} is the most used - " + \
        f"{map_sorted[0][1]} times."
    double_print(map_str, out_file_h)
    map_str = f"Least used map is {map_sorted[-1][0]} - only used {map_sorted[-1][1]} time(s)."
    double_print(map_str, out_file_h)

    scen_sorter = sorted(scenarios, key=lambda x: (x[3][2], x[3][1], x[3][0]))
    earliest_scenario = scen_sorter[0]
    earliest_scen_date = f"{month_map[earliest_scenario[3][0]]} {earliest_scenario[3][1]}, " + \
        f"{earliest_scenario[3][2]}"
    latest_scenario = scen_sorter[-1]
    earliest_scen_str = f"Earliest scenario is {earliest_scenario[0]} - {earliest_scen_date}"
    double_print(earliest_scen_str, out_file_h)

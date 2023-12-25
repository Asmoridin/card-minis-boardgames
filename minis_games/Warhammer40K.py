#!/usr/bin/python3

import sys, os

GAME_NAME = "Warhammer 40,000"
COMPANY = "Games Workshop"

my_armies = ['Adeptus Astartes', 'Necrons', ]

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('minis_games/DB/WH40KData.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/WH40KData.txt', 'r')
    sys.path.append('.')
    from utils.output_utils import double_print
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

total_max = 0
total_own = 0
errors = []
item_names = set()
army_points = {}
filter_lines = []
for line in lines:
    line = line.split('//')[0].strip()
    try:
        item_name, factions, keywords, points, item_own = line.split(';')
    except:
        print("Issue with line: " + line)
        continue
    item_names.add(item_name)
    factions = factions.split(',')
    factions = [faction.strip() for faction in factions]
    keywords = keywords.split(',')
    keywords = [kw.strip() for kw in keywords]
    points = int(points)
    try:
        item_own = float(item_own)
    except:
        item_own = int(item_own.split('/')[0])/int(item_own.split('/')[1])
    item_max = 3
    if 'Epic Hero' in keywords:
        item_max = 1
    elif 'Batteline' in keywords or 'Dedicated Transport' in keywords:
        item_max = 6
    total_max += item_max
    total_own += item_own

    for army in factions:
        if army not in army_points:
            army_points[army] = 0
    army_points[army] += points * item_own
    filter_lines.append((item_name, factions, keywords, points, item_own, item_max))

# Filter by army
armies = {}
for line in filter_lines:
    for army in line[1]:
        if army not in my_armies:
            continue
        if army not in armies:
            armies[army] = [0, 0]
        armies[army][1] += line[4]
        armies[army][0] += line[5]
army_sorter = []
for army in armies:
    army_sorter.append((army, armies[army][1]/armies[army][0], armies[army][0] - armies[army][1]))
army_sorter = sorted(army_sorter, key=lambda x:(x[1], -x[2], x[0]))

# Filter by keyword
keywords = {}
new_filter_lines = []
for line in filter_lines:
    if army_sorter[0][0] not in line[1]:
        continue
    for keyword in line[2]:
        if keyword not in item_names:
            if keyword not in keywords:
                keywords[keyword] = [0, 0]
            keywords[keyword][1] += line[4]
            keywords[keyword][0] += line[5]
    new_filter_lines.append(line)
filter_lines = new_filter_lines
keyword_sorter = []
for keyword in keywords:
    keyword_sorter.append((keyword, keywords[keyword][1]/keywords[keyword][0], keywords[keyword][0] - keywords[keyword][1]))
keyword_sorter = sorted(keyword_sorter, key=lambda x:(x[1], -x[2], x[0]))

# Sort by name
names = []
for line in filter_lines:
    if keyword_sorter[0][0] in line[2]:
        names.append((line[0], line[4]/line[5], line[5] - line[4]))
names = sorted(names, key=lambda x:(x[1], -x[2], x[0]))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("minis_games/output/Warhammer40K.txt", 'w')
    else:
        out_file_h = open("output/Warhammer40K.txt", 'w')
    for error in errors:
        double_print(error, out_file_h)
    double_print("I own %.2f out of %d - %.2f percent" % (total_own, total_max, 100 * total_own/total_max), out_file_h)

    status_string = "Buy a %s unit from the %s army, perhaps a %s" % (keyword_sorter[0][0], army_sorter[0][0], names[0][0])
    double_print(status_string, out_file_h)

    double_print("\nArmy points summary:", out_file_h)
    for army in sorted(army_points):
        if army_points[army] > 0:
            double_print(" - %s: %d" % (army, army_points[army]), out_file_h)

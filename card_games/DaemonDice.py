#!/usr/bin/python3

import sys, os

GAME_NAME = "Daemon Dice"

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/DaemonDiceData.txt', 'r')
else:
    file_h = open('DB/DaemonDiceData.txt', 'r')
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
total_max = 0
total_own = 0
for line in lines:
    dice_demon, dice_part, own = line.split(';')
    own = int(own)
    dice_max = max(own, 5)
    total_max += dice_max
    total_own += own
    item_list.append((dice_demon, dice_part, own, dice_max))

faction_map = {}
for item in item_list:
    if item[0] not in faction_map:
        faction_map[item[0]] = [0, 0]
    faction_map[item[0]][1] += item[3]
    faction_map[item[0]][0] += item[2]
faction_sorter = []
for key in faction_map:
    faction_sorter.append((key, faction_map[key][0]/faction_map[key][1], faction_map[key][1] - faction_map[key][0]))
faction_sorter = sorted(faction_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_faction = faction_sorter[0][0]
#print(chosen_faction)

filtered_list = []
part_map = {}
for item in item_list:
    if item[0] == chosen_faction:
        filtered_list.append(item)
        if item[1] not in part_map:
            part_map[item[1]] = [0, 0]
        part_map[item[1]][0] += 2
        part_map[item[1]][1] += 3
part_sorter = []
for key in part_map:
    part_sorter.append((key, part_map[key][0]/part_map[key][1], part_map[key][1] - part_map[key][0]))
part_sorter = sorted(part_sorter, key=lambda x:(x[1], -x[2], x[0]))
chosen_part = part_sorter[0][0]
#print(chosen_part)

pick_list = []
for item in filtered_list:
    if item[1] == chosen_part:
        pick_list.append(item)
pick_list = sorted(pick_list, key=lambda x:(x[2]/x[3], -1*(x[2]-x[2]), x[0] + ' ' + x[1]))
picked_item = pick_list[0]
#print(picked_item)

if __name__=="__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/DaemonDiceOut.txt", 'w')
    else:
        out_file_h = open("output/DaemonDiceOut.txt", 'w')

    print("Have %d out of %d - %.2f percent" % (total_own, total_max, 100*total_own/total_max))
    out_file_h.write("Have %d out of %d - %.2f percent\n" % (total_own, total_max, 100*total_own/total_max))

    print("Buy a %s (have %d out of %d)" % (picked_item[0] + ' ' + picked_item[1], picked_item[2], picked_item[3]))
    out_file_h.write("Buy a %s (have %d out of %d)\n" % (picked_item[0] + ' ' + picked_item[1], picked_item[2], picked_item[3]))

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")
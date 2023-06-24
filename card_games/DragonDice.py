#!/usr/bin/python3

import sys, os

GAME_NAME = "Dragon Dice"

army_factions = ['Dwarves', 'Coral Elves', 'Goblins', 'Lava Elves', 'Amazons', 'Fire Walkers', 'Undead', 'Feral', 'Swamp Stalkers', 'Frostwings', 'Scalders', 'Treefolk', 'Eldarim', 'Dracolem']
valid_factions = army_factions + ['Medallion', 'Items', 'Dragons', 'Dragonkin', 'Relics', 'Major Terrain', 'Minor Terrain', 'Special Terrain']

def getMetaType(in_type):
    if in_type in army_factions:
        return 'Unit'
    elif in_type in ['Special Terrain', 'Major Terrain', 'Minor Terrain']:
        return 'Terrain'
    elif in_type in ['Items', 'Medallion', 'Relics']:
        return 'Item'
    elif in_type in ['Dragons', 'Dragonkin']:
        return 'Dragon'
    else:
        print("Unhandled meta type: " + in_type)
        return('Unhandled')

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('card_games/DB/DragonDiceCollection.txt', 'r')
else:
    file_h = open('DB/DragonDiceCollection.txt', 'r')
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
total_max = 0
total_own = 0
faction_total = {}
for line in lines:
    dice_name, dice_faction, dice_size, own = line.split(';')
    if dice_faction not in valid_factions:
        print("Invalid faction: " + dice_faction)
    own = int(own)
    dice_max = 1
    if dice_faction not in faction_total:
        faction_total[dice_faction] = 0
    if dice_size == "Rare":
        if dice_faction in ['Items', 'Dragonkin']:
            dice_max = max(own, 1)
        else:
            dice_max = max(own, 2)
        faction_total[dice_faction] += (own * 3)
    elif dice_size == "Uncommon":
        if dice_faction in ['Items', 'Dragonkin']:
            dice_max = max(own, 2)
        else:
            dice_max = max(own, 4)
        faction_total[dice_faction] += (own * 2)
    elif dice_size == "Common":
        if dice_faction in ['Items', 'Dragonkin']:
            dice_max = max(own, 4)
        else:
            dice_max = max(own, 8)
        faction_total[dice_faction] += (own)
    elif dice_size == "Monster" or dice_size == "Champion" or dice_size == "Artifact" or dice_size == "Dragon":
        dice_max = max(own, 1)
        faction_total[dice_faction] += (own * 4)
    elif dice_faction == "Major Terrain":
        dice_max = max(own, 2)
    elif dice_faction in ['Minor Terrain', 'Special Terrain']:
        dice_max = max(own, 1)
    else:
        print("Unhandled dice size: " + dice_size)
    total_max += dice_max
    total_own += own
    item_list.append((dice_name, dice_faction, dice_size, own, dice_max))

if len(sys.argv) > 1 and sys.argv[1] == '-s':
    print("Summary:")
    for faction in sorted(army_factions):
        print("%s: %d" % (faction, faction_total[faction]))
    os._exit(0)
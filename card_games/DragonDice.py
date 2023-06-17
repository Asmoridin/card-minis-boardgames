#!/usr/bin/python3

import sys, os

GAME_NAME = "Dragon Dice"

def getMetaType(in_type):
    if in_type in ['Dwarves', 'Coral Elves', 'Goblins', 'Lava Elves', 'Amazons', 'Fire Walkers', 'Undead', 'Feral', 'Swamp Stalkers', 'Frostwings', 'Scalders', 'Treefolk', 'Eldarim', 'Dracolem']:
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
    
valid_factions = ['Dwarves', 'Coral Elves', 'Goblins', 'Lava Elves', 'Amazons', 'Fire Walkers', 'Undead', 'Feral', 'Swamp Stalkers', 'Frostwings', 'Scalders', 'Treefolk', 'Eldarim', 
    'Dracolem', 'Medallion', 'Items', 'Dragons', 'Dragonkin', 'Relics', 'Major Terrain', 'Minor Terrain', 'Special Terrain']

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
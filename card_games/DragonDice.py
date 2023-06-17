#!/usr/bin/python3

import sys, os

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

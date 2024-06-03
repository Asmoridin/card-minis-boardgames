#!/usr/bin/python3

"""
Collection manager and tracker for the Battletech miniatures game
"""

import os
import sys

GAME_NAME = "Battletech"
COMPANY = "Catalyst"

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('minis_games/DB/BattletechOwn.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/BattletechOwn.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

def get_max(input_item):
    """
    Return the maximum amount of an item I'd like to own (mostly 1)
    """
    if input_item in ['Mech', 'Vehicle', 'Aerospace', ]:
        return 1
    elif input_item in ['Battle Armor', ]:
        return 4 # 6 in Alpha Strike
    else:
        print("Unknown max: " + input_item)
        return 1

def getMetaType(in_type):
    """
    For an item type, return a more general type
    """
    if in_type in ['Heavy Vehicle', 'Medium Vehicle', 'Light Vehicle', 'Assault Vehicle', ]:
        return("Vehicle")
    elif in_type in ['Light Mech', 'Medium Mech', 'Assault Mech', 'Heavy Mech', ]:
        return("Mech")
    elif in_type in ['Light Battle Armor', 'Medium Battle Armor', 'Assault Battle Armor', 'Heavy Battle Armor', ]:
        return ("Battle Armor")
    elif in_type in ['Light Aerospace', 'Heavy Aerospace', 'Conventional Fighter', 'Medium Aerospace', ]:
        return("Aerospace")
    else:
        print("Unknown meta tpe: " + in_type)
        return("")

valid_model_types = ['Heavy Vehicle', 'Medium Vehicle', 'Medium Mech', 'Light Mech', 'Assault Mech', 'Light Battle Armor', 'Heavy Mech', 'Light Vehicle', 'Medium Battle Armor',
        'Light Aerospace',  'Conventional Fighter', 'Assault Vehicle', 'Heavy Aerospace', 'Medium Aerospace', 'Assault Battle Armor', 'Heavy Battle Armor']
eras = ['Age of War (2005 - 2570)', 'Star League (2571 - 2780)', 'Early Succession War (2781 - 2900)', 'Late Succession War - LosTech (2901 - 3019)', 
        'Late Succession War - Renaissance (3020 - 3049)', 'Clan Invasion (3050 - 3061)', 'Civil War (3062 - 3067)', 'Jihad (3068 - 3080)', 'Early Republic (3081 - 3100)', 
        'Late Republic (3101 - 3130)', 'Dark Age (3131 - 3150)', ]
roles = ['Juggernaut', 'Sniper', 'Scout', 'Ambusher', 'Brawler', 'Missile Boat', 'Skirmisher', 'Striker', 'None', 'Interceptor', 'Attack', 'Dogfighter', 'Fire-Support', 
         'Fast Dogfighter']
source_documents = ['3039', '3050', '3058', 'ilClan Vol. 5', ]

total_max = 0
total_own = 0
mini_lines = []
filter_lines = []
errors = []

for line in lines:
    if line == '' or line.startswith('#'):
        continue
    try:
        mini_name, tech_base, model_type, model_era, chassis, role, source_doc, own_amount = line.split(';')
    except:
        errors.append("Problem with line:")
        errors.append(line)
        continue
    if tech_base not in ['Inner Sphere', 'Clan', 'Mixed']:
        errors.append("Invalid tech base %s" % tech_base)
        errors.append('Relevant line: ' + line)
    if model_type not in valid_model_types:
        errors.append("Possibly invalid model type: %s" % model_type)
        errors.append('Relevant line: ' + line)
    if model_era not in eras:
        errors.append("Invalid model era: %s" % model_era)
        errors.append('Relevant line: ' + line)
    if role not in roles:
        errors.append("Invalid role: %s" % role)
        errors.append('Relevant line: ' + line)
    if source_doc not in source_documents:
        errors.append("Invalid source doc: %s" % source_doc)
        errors.append('Relevant line: ' + line)
    own_amount = int(own_amount)
    max_amount = max(own_amount, 1, get_max(getMetaType(model_type)))
    total_own += own_amount
    total_max += max_amount
    
if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("minis_games/output/BattletechOut.txt", 'w')
    else:
        out_file_h = open("output/BattletechOut.txt", 'w')
    for error in errors:
        double_print(error, out_file_h)
    double_print("I own %d out of %d - %.2f percent" % (total_own, total_max, 100 * total_own/total_max), out_file_h)

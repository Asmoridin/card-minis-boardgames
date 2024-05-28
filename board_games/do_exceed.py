#!/usr/bin/python3

"""
Script that generates groups for a future Exceed tournament
"""

import math
import random
import os

red_horizon = ['Eva', 'Kaden', 'Miska', 'Lily', 'Reese', 'Heidi', 'Vincent', 'Nehtali', \
    'Satoshi', 'Mei-Lien', 'Baelkhor', 'Morathi', 'Gabrek', 'Ulrik', 'Alice', 'Zoey', ]#16
seventh_cross = ['Geoffrey', 'Celinka', 'Taisei', "D'Janette", 'ZSolt', 'Renea', 'Minato', \
    'Tournelouse', 'Eugenia', 'Galdred', 'Umina', 'Remiliss', 'Luciya', 'Syrus', 'Seijun', \
    'Iaquis', 'Emogine', 'Sydney & Serena', ] #18
promo = ['Juno', 'Devris', 'Super Skull Man 33', 'Carl Swangee', 'Pooky', 'Shovel Knight', 'Fight', 'The Beheaded'] #8
street_fighter = ['Sagat', 'Ryu', 'Akuma', 'Zangief', 'Vega', 'C.Viper', 'Chun-Li', 'Dan', 'Cammy', 'M. Bison', 'Ken', 'Guile', ] #12
shovel_knight = ['Shovel Knight & Shield Knight', 'Propeller Knight', 'Mole Knight', 'Tinker Knight', 'Plague Knight', 'Polar Knight', 'Treasure Knight', 'King Knight', 'The Enchantress', 'Specter Knight', ] #10
blazblue = ['Ragna', 'Tager', 'Taokaka', 'Rachel', 'Jin', 'Hakumen', 'Carl', 'Bang', 'Noel', 'Nu-13', 'Arakune', 'Litchi', 'Hazama', 'Nine the Phantom', 'Platinum the Trinity', 'Kokonoe', ] #16
under_night = ['Yuzuriha', 'Carmine', 'Byakuya', 'Mika', 'Gordeau', 'Chaos', 'Hilda', 'Phonon', 'Seth', 'Enkdu', 'Vatista', 'Nanase', 'Orie', 'Waldstein', 'Merkava', 'Wagner', 'Hyde', 'Linne', 'Londrekia', ] #19
guilty_gear = ['Sol Badguy', 'Ky Kiske', 'May', 'Axl Low', 'Chipp Zanuff', 'Potemkin', 'Faust', 'Millia Rage', 'Zato-1', 'Ramlethal Valentine', 'I-No', 'Nagoriyuki', 'Giovanna', 'Anji Mito', 'Leo Whitefang', 'Jack-O', 'Goldlewis Dickinson', 'Happy Chaos', 'Baiken', 'Testament', ] # 20

fighters = sorted(red_horizon + seventh_cross + promo + street_fighter + shovel_knight + blazblue + under_night + guilty_gear)

def genGroups(numberOfGroups):
    groups = []
    for group_name in [red_horizon, seventh_cross, promo, street_fighter, shovel_knight, blazblue, under_night, guilty_gear]:
        random.shuffle(group_name)
    fighter_order = red_horizon + seventh_cross + promo + street_fighter + shovel_knight + blazblue + under_night + guilty_gear
    for group_num in range(0, numberOfGroups):
        this_group = []
        counter = group_num
        while counter <len(fighters):
            this_group.append(fighter_order[counter])
            counter += numberOfGroups
        groups.append(this_group)
    return(groups)

if __name__ == "__main__":
    for group in genGroups(8):
        print(group)
    print("\nTotal: %d Fighters, and %d combinations" % (len(fighters), math.comb(len(fighters), 2)))
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

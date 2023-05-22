#!/usr/bin/python3

import random, math

red_horizon = ['Eva', 'Kaden', 'Miska', 'Lily', 'Reese', 'Heidi', 'Vincent', 'Nehtali', ]
seventh_cross = ['Geoffrey', ]
promo = ['Juno', ]
street_fighter = ['Sagat', ]
shovel_knight = ['Shovel Knight & Shield Knight', ]
blazblue = ['Ragna', ]
under_night = ['Yuzuriha', ]

fighters = sorted(red_horizon + seventh_cross + promo + street_fighter + shovel_knight + blazblue + under_night)

def genGroups(numberOfGroups):
    groups = []
    for group_name in [red_horizon, seventh_cross, promo, street_fighter, shovel_knight, blazblue, under_night]:
        random.shuffle(group_name)
    fighter_order = red_horizon + seventh_cross + promo + street_fighter + shovel_knight + blazblue + under_night
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
#!/usr/bin/python3

"""
Basic library that has data about the races of Star Fleet Battles
"""

alpha_races = ['Federation', 'Klingon', 'Kzinti', 'Hydran', 'WYN', 'Romulan', 'Andromedan',
    'Orion', 'Gorn', 'Tholian', 'ISC', 'Lyran', 'LDR', 'Vudar', 'Jindarian', 'Nicozian', 'Borak',
    'Carnivon', 'Paravian', 'Peladine', 'Seltorian']
simulator_races = ['Barbarian', 'Britanian', "Cana'dien", 'Deltan', 'Flivver', 'Frax',
    'Hispaniolan', 'Qari', 'Sharkhunter', 'Triaxian', '8th Air Force']
omega_races = ['Alunda', 'FRA', 'Bolosco', 'Branthodon', 'Chlorophon', 'Drex', 'Hiver', 'Iridani',
    'Koligahr', 'Loriyill', 'Maesron', 'Probr', 'Qixa', 'Ryn', 'Sigvirion', 'Singer', 'Souldra',
    'Trobrin', 'Vari', 'Worb', 'Ymatrian', 'Zosman']
lmc_races = ['Baduvai', 'Eneen', 'Jumokian', 'Maghadim', 'Uthiki']
triangulum_races = ['Helgardian', 'Arachnid', 'Mallaran', 'Imperium']

all_race_names = alpha_races + simulator_races + omega_races + lmc_races + triangulum_races

race_map = {'Alpha':alpha_races, 'Omega':omega_races, 'Simulator':simulator_races,
    'LMC':lmc_races, 'Triangulum':triangulum_races}

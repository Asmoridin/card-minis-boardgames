#!/usr/bin/python3

import itertools

modular_encounters = ['Bomb Scare', 'Masters of Evil', 'Under Attack', 'Legions of Hydra', 'The Doomsday Chair', 'A Mess of Things', 'Goblin Gimmicks', 'Power Drain', 'Running Interference',
    'Hydra Assault', 'Weapon Master', 'Hydra Patrol', 'Master of Time', 'Anachronauts', 'Temporal', 'Kree Fanatic', 'Experimental Weapons',
    'Band of Badoon', 'Galactic Artifacts', 'Kree Militants', 'Menagerie Medley', 'Space Pirates', 'Badoon Headhunter', 'Power Stone', 'Ship Command',
    'Infinity Gauntlet', 'Black Order', 'Armies of Titan', 'Children of Thanos', 'Legions of Hel', 'Frost Giants', 'Enchantress', 
    'Beasty Boys', 'Mister Hyde', 'Sinister Syndicate', "Crossfire's Crew", 'Wrecking Crew', 'Ransacked Armory', 'State of Emergency', 'Streets of Mayhem', 'Brothers Grimm',
    'Guerilla Tactics', 'Sinister Assault', 'City in Chaos', 'Down to Earth', 'Symbiotic Strength', 'Personal Nightmare', 'Whispers of Paranoia', 'Goblin Gear', 'Osborn Tech',
    'Armadillo', 'Zzzax', 'The Inheritors', "Iron Spider's Sinister Six", 'Deathstrike', 'Shadow King', 'Exodus', 'Reavers', 
    'Zero Tolerance', 'Sentinels', 'Future Past', 'Brotherhood', 'Mystique', 'Acolytes', ]
mojo_encounters = ['Crime', 'Fantasy', 'Horror', 'Sci-Fi', 'Sitcom', 'Western']
modular_encounters = modular_encounters + mojo_encounters

encounters = []
def get_req_by_encounter(encounter_set):
    for encounter in encounters:
        if encounter.name == encounter_set:
            return encounter.required_encounters
        
class Encounter:
    def __init__(self, name, num_encounters, required_enc=[], can_infinity=True, mojo_only=False):
        self.name = name
        if type(num_encounters) != type(0):
            raise ValueError("Invalid modular encounter count")
        self.num_encounters = num_encounters
        self.required_encounters = required_enc
        for encounter in self.required_encounters:
            if encounter not in modular_encounters:
                raise ValueError("Invalid required encounter: " + encounter)
        self.can_infinity = can_infinity
        self.mojo_only = mojo_only
    def genCombos(self):
        ret_list = []
        if self.mojo_only:
            modular_combos = itertools.combinations(mojo_encounters, self.num_encounters)
        else:
            modular_combos = itertools.combinations(modular_encounters, self.num_encounters)
        for modular_combo in modular_combos:
            valid = True
            for req_enc in self.required_encounters:
                if req_enc in modular_combos:
                    valid = False
            if not self.can_infinity and 'Infinity Gauntlet' in modular_combo:
                valid = False
            if valid:
                ret_list.append((self.name, tuple(sorted(modular_combo))))
        return(ret_list)
    

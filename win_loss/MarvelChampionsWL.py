#!/usr/bin/python3

import random, math, itertools, os

from Libraries import MarvelChampionsEncounters as ChampEncounters
from Libraries import MarvelChampionsHeroes as ChampHeroes

total_hero_choices = len(ChampHeroes.hero_combinations)

def getHeroWL(hero, aspect, playMap):
    wins = 0
    losses = 0
    if (hero, aspect) in playMap:
        wins = playMap[(hero, aspect)][1]
        losses = playMap[(hero, aspect)][0] - wins
    return((wins, losses))

def getEncounterWL(encounter, mod_encounters, encounter_map):
    wins = 0
    losses = 0
    mod_encounters = tuple(sorted(mod_encounters))
    if (encounter, mod_encounters) in encounter_map:
        wins = encounter_map[(encounter, mod_encounters)][1]
        losses = encounter_map[(encounter, mod_encounters)][0] - wins
    return((wins, losses))

def determineCombinations():
    # This is the number of different hero combinations I can play.
    combinations = set()
    h_1 = ChampHeroes.hero_combinations
    h_2 = ChampHeroes.hero_combinations
    for combo_1 in h_1:
        for combo_2 in h_2:
            if combo_1[0] != combo_2[0] and combo_1[1] != combo_2[1]:
                this_combo = sorted([combo_1, combo_2])
                combinations.add(tuple(this_combo))
    return(len(combinations))

def getHeroStats(playMap):
    # Return the following = most played hero, most played hero amount, least played hero, least played hero amount
    sum_map = {} # Need to sum up the plays by each hero
    for hero in ChampHeroes.heroes:
        sum_map[hero.name] = 0
    for (hero, aspect) in playMap:
        sum_map[hero] += playMap[(hero, aspect)][0]
    hero_list = []
    for hero in sum_map:
        hero_list.append((hero, sum_map[hero]))
    hero_list = sorted(hero_list, key=lambda x:(x[1], x[0]))
    return(hero_list[-1][0], hero_list[-1][1], hero_list[0][0], hero_list[0][1])

def getAspectStats(playMap):
    # Return most played aspect, amount of times played said aspect, least played aspect, amount of plays for that aspect
    sum_map = {}
    for aspect in ChampHeroes.aspects:
        sum_map[aspect] = 0
    for (hero, aspect_tuple) in playMap:
        for aspect in aspect_tuple:
            sum_map[aspect] += playMap[(hero, aspect_tuple)][0]
    # TODO: Tuple the sum map, sort it
    print("Aspect sorting to do")
    print(sum_map)
    return()

def getLeastPlayedHero(playMap):
    # Return the least played hero/aspect combination
    least_played_hero = getHeroStats(playMap)[2]
    combinations = ChampHeroes.hero_map[least_played_hero].genCombos()
    print(combinations)
    # TODO: Finish this.  Basically, find the least played hero-aspect comination
    return("Rogue", "Justice")

def getLeastPlayedEncounter(enc_played_map):
    # Return the encounter combination played the least
    return(("Rhino", "Bomb Scare"))

def getVillainStats(encounter_map):
    # Returns (most played villain, most played villain amount, least played villain, least played villain amount)
    sum_map = {}
    for villain in ChampEncounters.encounters:
        sum_map[villain.name] = 0
    # TODO: Do the calculations, sort it, and figure it out
    return("Klaw", 100, 'Rhino', 0)

def getModularStats(encounter_map):
    # Return most played encounter set, amount it was played, least played encounter set, amount played
    modular_sets = ChampEncounters.modular_encounters
    sum_map = {}
    for modular in modular_sets:
        sum_map[modular] = 0
    #TODO: tuple it, sort it, return it
    return("Ship Command", 100, "Inheritors", 0)

# Read in and set up Hero data structures
if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('win_loss/DB/ChampionsPlayedHeroes.txt', 'r')
else:
    file_h = open('DB/ChampionsPlayedHeroes.txt', 'r')
hero_lines = file_h.readlines()
file_h.close()
hero_lines = [line.strip() for line in hero_lines]
hero_played_map = {}
played_max = 0
for line in hero_lines:
    hero_line = line.split(';')
    if int(hero_line[2]) > played_max:
        played_max = int(hero_line[2])
    aspects = ()
    if hero_line[1] != '':
        aspects = tuple(hero_line[1].split('/'))
    hero_played_map[(hero_line[0], aspects)] = (int(hero_line[2]), int(hero_line[3]))

if __name__ == "__main__":
    print("Generating a game")
    print("There are %d different Hero/Aspect combinations, and %d different game pairings" % (total_hero_choices, determineCombinations()))
    
    print("Currently have played %.1f percent of Hero/Aspects" % (len(hero_played_map) * 100 / total_hero_choices))
    print("There are %d heroes, %d different encounters, and %d different modular encounter sets\n" % (len(ChampHeroes.heroes), len(ChampEncounters.encounters), len(ChampEncounters.modular_encounters)))

    # Choose first hero - always choose least played hero
    choice_1 = getLeastPlayedHero(hero_played_map)

    # Choose second hero, with lowest hero/aspect combination remaining
    
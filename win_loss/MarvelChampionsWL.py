#!/usr/bin/python3

import random, math, itertools

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
                combinations.add(this_combo)
    return(len(combinations))

def getHeroStats(playMap):
    # Return the following = most played hero, most played hero amount, least played hero, least played hero amount
    sum_map = {} # Need to sum up the plays by each hero
    for hero in ChampHeroes.heroes:
        sum_map[hero.name] = 0
    for (hero, aspect) in playMap:
        sum_map[hero] += playMap[(hero, aspect)][0]
    #TODO: Tuple the sum map, sort it
    print("Work to do here")
    print(sum_map)
    return('Rogue', 0, 'Rogue', 0)

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
    least_played_hero = getHeroStats(playMap)[0]
    combinations = ChampHeroes.hero_map[least_played_hero].genCombos()
    print(combinations)
    # TODO: Finish this.  Basically, find the least played 
#!/usr/bin/python3

"""
List wins and losses for Marvel Champions, and give recommendations for what to play next
"""

import os
import random
import sys

if os.getcwd().endswith('card-minis-boardgames'):
    sys.path.append('.')
    from utils.output_utils import double_print
    file_h = open('win_loss/DB/ChampionsPlayedHeroes.txt', 'r', encoding="UTF-8")
    enc_file_h = open('win_loss/DB/ChampionsPlayedEncounters.txt', 'r', encoding="UTF-8")
else:
    sys.path.append('.')
    from utils.output_utils import double_print
    file_h = open('DB/ChampionsPlayedHeroes.txt', 'r', encoding="UTF-8")
    enc_file_h = open('DB/ChampionsPlayedEncounters.txt', 'r', encoding="UTF-8")

from Libraries import MarvelChampionsEncounters as ChampEncounters
from Libraries import MarvelChampionsHeroes as ChampHeroes

total_hero_choices = len(ChampHeroes.hero_combinations)

def get_hero_wl(in_hero, in_aspect, in_play_map):
    """
    For a given hero and aspect, return the total wins and losses
    """
    hero_wins = 0
    hero_losses = 0
    if (in_hero, in_aspect) in in_play_map:
        hero_wins = in_play_map[(in_hero, in_aspect)][1]
        hero_losses = in_play_map[(in_hero, in_aspect)][0] - hero_wins
    return((hero_wins, hero_losses))

def getEncounterWL(encounter, mod_encounters, encounter_map):
    wins = 0
    losses = 0
    mod_encounters = tuple(sorted(mod_encounters))
    if (encounter, mod_encounters) in encounter_map:
        wins = encounter_map[(encounter, mod_encounters)][1]
        losses = encounter_map[(encounter, mod_encounters)][0] - wins
    return((wins, losses))

def determine_combinations():
    """
    Return the number of different hero combinations I can play.
    """
    combinations = set()
    h_1 = ChampHeroes.hero_combinations
    h_2 = ChampHeroes.hero_combinations
    for combo_1 in h_1:
        for combo_2 in h_2:
            if combo_1[0] != combo_2[0] and combo_1[1] != combo_2[1]:
                this_combo = sorted([combo_1, combo_2])
                combinations.add(tuple(this_combo))
    return len(combinations)

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

    aspect_tuples = []
    for aspect in sum_map:
        aspect_tuples.append((aspect, sum_map[aspect]))
    aspect_tuples = sorted(aspect_tuples, key=lambda x:(x[1], x[0]))
    return(aspect_tuples[-1][0], aspect_tuples[-1][1], aspect_tuples[0][0], aspect_tuples[0][1])

def getLeastPlayedHero(playMap):
    # Return the least played hero/aspect combination
    least_played_hero = getHeroStats(playMap)[2]
    combinations = ChampHeroes.hero_map[least_played_hero].genCombos()
    aspect_combos = []
    for combination in combinations:
        if combination not in playMap:
            aspect_combos.append((combination, 0))
        else:
            aspect_combos.append((combination, playMap[combination]))
    aspect_combos = sorted(aspect_combos, key=lambda x:(x[1], x[0][1]))
    return(aspect_combos[0][0][0], aspect_combos[0][0][1])

def getLeastPlayedEncounter(enc_played_map):
    # First, get least played villain
    chosen_villain = getVillainStats(enc_played_map)[2]
    if chosen_villain == 'The Hood':
        hood_encounters = sorted(random.sample(ChampEncounters.modular_encounters, 7))
        this_encounter = ('The Hood', tuple(hood_encounters))
        return this_encounter
    encounter_list = ChampEncounters.encounter_map[chosen_villain].genCombos()
    encounter_list = sorted(encounter_list, key=lambda x:x[1])
    encounter_played = []
    for encounter_combo in encounter_list:
        if encounter_combo not in enc_played_map:
            return encounter_combo
        encounter_played.append((encounter_combo, enc_played_map[encounter_combo][0]))
    encounter_played = sorted(encounter_played, key=lambda x: x[1])
    return encounter_played[0][0]

def getVillainStats(encounter_map):
    # Returns (most played villain, most played villain amount, least played villain, least played villain amount)
    sum_map = {}
    for villain in ChampEncounters.encounters:
        sum_map[villain.name] = 0
    for played_enc in encounter_map:
        sum_map[played_enc[0]] += encounter_map[played_enc][0]
    sum_tuples = []
    for villain in sum_map:
        sum_tuples.append((villain, sum_map[villain]))
    sum_tuples = sorted(sum_tuples, key=lambda x:(x[1], x[0]))
    return(sum_tuples[-1][0], sum_tuples[-1][1], sum_tuples[0][0], sum_tuples[0][1])

def getModularStats(encounter_map):
    # Return most played encounter set, amount it was played, least played encounter set, amount played
    modular_sets = ChampEncounters.modular_encounters
    sum_map = {}
    for modular in modular_sets:
        sum_map[modular] = 0
    for played_enc in encounter_map:
        for modular in ChampEncounters.get_req_by_encounter(played_enc[0]):
            sum_map[modular] += encounter_map[played_enc][0]
        for modular in played_enc[1]:
            sum_map[modular] += encounter_map[played_enc][0]
    mod_tuples = []
    for modular in sum_map:
        mod_tuples.append((modular, sum_map[modular]))
    mod_tuples = sorted(mod_tuples, key=lambda x:(x[1], x[0]))
    return(mod_tuples[-1][0], mod_tuples[-1][1], mod_tuples[0][0], mod_tuples[0][1])

# Read in and set up Hero data structures
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

# Read in and process the Encounter data structures
encounter_lines = enc_file_h.readlines()
enc_file_h.close()
encounter_lines = [line.strip() for line in encounter_lines]
enc_played_map = {}
played_max = 0
for line in encounter_lines:
    #TODO: encounter_line[2] is the difficulty, do we want to do anything with it?
    encounter_line = line.split(';')
    if int(encounter_line[3]) > played_max:
        played_max = int(encounter_line[3])
    encounter_sets = tuple(sorted(encounter_line[1].split('/')))
    if encounter_sets == ('',):
        encounter_sets = ()
    enc_played_map[(encounter_line[0], encounter_sets)] = (int(encounter_line[3]), int(encounter_line[4]))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("win_loss/output/MarvelChampionsOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/MarvelChampionsOut.txt", 'w', encoding="UTF-8")
    double_print("Generating a game", out_file_h)
    double_print("There are %d different Hero/Aspect combinations, and %d different game pairings" % (total_hero_choices, determine_combinations()), out_file_h)

    double_print("Currently have played %.1f percent of Hero/Aspects" % (len(hero_played_map) * 100 / total_hero_choices), out_file_h)
    double_print("There are %d heroes, %d different encounters, and %d different modular encounter sets\n" % (len(ChampHeroes.heroes), len(ChampEncounters.encounters), len(ChampEncounters.modular_encounters)), out_file_h)

    # Choose first hero - always choose least played hero
    choice_1 = getLeastPlayedHero(hero_played_map)

    # Choose second hero, with lowest hero/aspect combination remaining
    choices = []
    for hero_choice in ChampHeroes.hero_combinations:
        if hero_choice[0] == choice_1[0]:
            continue
        VALID = True
        for aspect in hero_choice[1]:
            if aspect in choice_1[1]:
                VALID = False
        if not VALID:
            continue
        if (hero_choice[0], hero_choice[1]) in hero_played_map:
            choices.append((hero_choice[0], hero_choice[1], hero_played_map[(hero_choice[0], hero_choice[1])][0]))
        else:
            choices.append((hero_choice[0], hero_choice[1], 0))
    choices = sorted(choices, key=lambda x:(x[2], x[0], x[1]))
    choice_2 = (choices[0][0], choices[0][1])

    hero_tuple = getHeroStats(hero_played_map)
    double_print("Most played hero: %s (%d times). Least: %s (%d)" % (hero_tuple), out_file_h)
    aspect_tuple = getAspectStats(hero_played_map)
    double_print("Most played aspect: %s (%d times). Least: %s (%d)" % (aspect_tuple), out_file_h)
    scenario_tuple = getVillainStats(enc_played_map)
    double_print("Most played scenario: %s (%d times). Least: %s (%d)" % (scenario_tuple), out_file_h)
    modular_tuple = getModularStats(enc_played_map)
    double_print("Most played modular encounter: %s (%d times). Least: %s (%d)" % (modular_tuple), out_file_h)

    # Choose an encounter
    encounter_choice = getLeastPlayedEncounter(enc_played_map)

    hero_1_wl = get_hero_wl(choice_1[0], choice_1[1], hero_played_map)
    hero_2_wl = get_hero_wl(choice_2[0], choice_2[1], hero_played_map)
    double_print("\nHeroes/Aspects chosen: %s %s (%sW-%sL) and %s %s (%sW-%sL)" % ('/'.join(choice_1[1]), choice_1[0], hero_1_wl[0], hero_1_wl[1], '/'.join(choice_2[1]), choice_2[0], hero_2_wl[0], hero_2_wl[1]), out_file_h)
    enc_wl = getEncounterWL(encounter_choice[0], encounter_choice[1], enc_played_map)
    double_print("Chosen encounter is %s %s (%sW-%sL)" % ('/'.join(encounter_choice[1]), encounter_choice[0], enc_wl[0], enc_wl[1]), out_file_h)

    double_print("\nTotal W-L by hero:", out_file_h)
    hero_wl = {}
    for hero_choice in ChampHeroes.hero_combinations:
        if hero_choice[0] not in hero_wl:
            hero_wl[hero_choice[0]] = [0,0]
        wins, losses = get_hero_wl(hero_choice[0], hero_choice[1], hero_played_map)
        hero_wl[hero_choice[0]][0] += wins
        hero_wl[hero_choice[0]][1] += losses
    for hero in sorted(hero_wl):
        double_print("%s%s%d - %d" % (hero, " " * (30 - len(hero)), hero_wl[hero][0], hero_wl[hero][1]), out_file_h)

    overall_wl = [0, 0]
    double_print("\nTotal W-L by villain:", out_file_h)
    villain_wl = {}
    for villain_choice in enc_played_map:
        if villain_choice[0] not in villain_wl:
            villain_wl[villain_choice[0]] = [0,0]
        wins, losses = getEncounterWL(villain_choice[0], villain_choice[1], enc_played_map)
        villain_wl[villain_choice[0]][0] += wins
        overall_wl[0] += wins
        villain_wl[villain_choice[0]][1] += losses
        overall_wl[1] += losses

    for villain in sorted(villain_wl):
        double_print("%s%s%d - %d" % (villain, " " * (30-len(villain)), villain_wl[villain][0], villain_wl[villain][1]), out_file_h)

    double_print("\nTotal W-L by aspect:", out_file_h)
    aspect_wl = {}
    for hero_choice in ChampHeroes.hero_combinations:
        for aspect in hero_choice[1]:
            if aspect not in aspect_wl:
                aspect_wl[aspect] = [0,0]
            wins, losses = get_hero_wl(hero_choice[0], hero_choice[1], hero_played_map)
            aspect_wl[aspect][0] += wins
            aspect_wl[aspect][1] += losses
    double_print(str(aspect_wl), out_file_h)

    double_print("\nWin Loss Records, Overall: %d - %d, %.3f" % (overall_wl[0], overall_wl[1], overall_wl[0]/(overall_wl[0] + overall_wl[1])), out_file_h)
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")
#!/usr/bin/python3

"""
Collection tracker, and purchase suggestion tool for Marvel Crisis Protocol
"""

import os
import sys

GAME_NAME = "Marvel Crisis Protocol"
COMPANY = "AMG"

if os.getcwd().endswith('card-minis-boardgames'):
    file_h = open('minis_games/DB/MCPData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print
else:
    file_h = open('DB/MCPData.txt', 'r', encoding="UTF-8")
    sys.path.append('.')
    from utils.output_utils import double_print

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

valid_affiliations = ['Avengers', 'Hydra', 'Cabal', 'A-Force', 'Inhumans', 'X-Force',
    'Black Order', 'Defenders', 'Web Warriors', 'Convocation', 'Uncanny X-Men', 'Winter Guard',
    'Criminal Syndicate', 'Weapon X', 'Guardians of the Galaxy', 'Sentinels', 'Spider-Foes', 
    'S.H.I.E.L.D.', 'Asgard', 'Midnight Sons', 'Brotherhood of Mutants', 'Wakanda',
    'Dark Dimension', ]

data = []
leaders = {}
affiliated_models = {}
for affiliation in valid_affiliations:
    leaders[affiliation] = []
    affiliated_models[affiliation] = []
TOTAL_MAX = 0
TOTAL_OWN = 0
for line in lines:
    model_name, model_affils, model_own = line.split(';')
    model_affils = model_affils.split(',')
    model_affils = [affiliation.strip() for affiliation in model_affils]
    for affiliation in model_affils:
        cleaned_affil = affiliation.replace("/L", '')
        if cleaned_affil not in valid_affiliations:
            print(f"Invalid affiliation: {affiliation}")
            continue
        if "/L" in affiliation:
            leaders[cleaned_affil].append(model_name)
            affiliated_models[cleaned_affil].append(model_name)
        else:
            affiliated_models[affiliation].append(model_name)

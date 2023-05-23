#!/usr/bin/python3

valid_houses = ['Brobnar', 'Mars', 'Untamed', 'Logos', 'Sanctum', 'Shadows', 'Star Alliance', 'Dis', 'Saurian Republic', 'Unfathomable', ] # Ekwidon
valid_sets = ['Call of the Archons', 'Worlds Collide', 'Age of Ascension', 'Mass Mutations', 'Dark Tidings', ] # Winds of someting

deck_info = open('DB/KeyForgeDecks.txt', 'r')
wl_info = open('DB/KeyForgeWLData.txt', 'r')

my_decks = []

class Deck:
    def __init__(self, short_name, name, game_set, houses, notes):
        self.short_name = short_name
        self.name = name
        if game_set in valid_sets:
            self.game_set = game_set
        else:
            print('Invalid set: ' + game_set)
        self.houses = set()
        for house in houses.split(','):
            if house.strip() not in valid_houses:
                print("Invalid house: " + house.strip())
            else:
                self.houses.add(house.strip())
        self.deck_note = notes
        self.games = 0
        self.wins = 0
        self.losses = 0
    def __str__(self):
        return "Deck: %s, Houses: %s, Record: %d-%d, Note: %s" % (self.name, ', '.join(self.houses), self.wins, self.losses, self.deck_note)
    
def getDeck(name):
    for deck in my_decks:
        if deck.name == name:
            return deck
    return None

deck_lines = deck_info.readlines()
wl_lines = wl_info.readlines()

# House frequency map, both owned and played
# Figure out set I own the least from.
# FIgure out least played deck.
# Figure out deck I'm most successful with.
# Output least owned house, and least owned set.
# Output least played deck, with number of games.
# OUput most successful deck, with win loss record.
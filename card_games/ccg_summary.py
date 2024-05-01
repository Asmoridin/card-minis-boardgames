#!/usr/bin/python3

"""
Summarizes the current collection status of all tracked card/dice games
"""

import os
import sys

import city_of_heroes
import DaemonDice
import DragonDice
import StarTrekSecondEdition
import Tribbles
import anachronism
import card_games.star_wars_unlimited as star_wars_unlimited

if os.getcwd().endswith('card-minis-boardgames'):
    sys.path.append('.')
    from utils.output_utils import double_print
    in_file = open("card_games/DB/NewCardGames.txt", encoding="UTF-8")
else:
    sys.path.append('.')
    from utils.output_utils import double_print
    in_file = open("DB/NewCardGames.txt", encoding="UTF-8")

#print("\033[96mTest.\033[0m")

started_games = [anachronism, DaemonDice, DragonDice, star_wars_unlimited, StarTrekSecondEdition,
    Tribbles, city_of_heroes]

TOTAL_HAVE = 0
TOTAL_MAX = 0
NEW_GAMES_STARTED = 1 + len(started_games)
game_data = []

other_games = in_file.readlines()
in_file.close()
other_games = [line.strip() for line in other_games]

new_games_count = len(other_games) + NEW_GAMES_STARTED

for game in started_games:
    TOTAL_HAVE += game.TOTAL_OWN
    TOTAL_MAX += game.TOTAL_MAX
    game_data.append((game.GAME_NAME, game.TOTAL_OWN, game.TOTAL_MAX))

game_data.append(("New Game", NEW_GAMES_STARTED + 1, new_games_count + 1))
game_data = sorted(game_data, key=lambda x:(x[1]/x[2], -1 * (x[2] - x[1])))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/CCGSummaryOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("output/CCGSummaryOut.txt", 'w', encoding="UTF-8")
    total_percentage = TOTAL_HAVE * 100 /TOTAL_MAX
    total_string = f"Totaling {len(game_data) - 1} games, owning {TOTAL_HAVE} out of {TOTAL_MAX} cards/dice ({total_percentage:.2f} percent)"
    double_print(total_string, out_file_h)
    lowest_game_percentage = game_data[0][1]*100/game_data[0][2]
    lowest_game_string = f"Lowest game is {game_data[0][0]} at {lowest_game_percentage:.2f} percent ({game_data[0][1]} / {game_data[0][2]})"
    double_print(lowest_game_string, out_file_h)
    next_lowest_percentage = game_data[1][1] * 100 / game_data[1][2]
    next_lowest_string = f"- (Next lowest game is {next_lowest_percentage:.2f} percent)"
    double_print(next_lowest_string, out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

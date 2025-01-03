#!/usr/bin/python3

"""
Summarizes the current collection status of all tracked card/dice games
"""

import os
import sys
sys.path.append('.')

import card_games.anachronism as anachronism
import card_games.wyvern as wyvern
import card_games.dbs_fusion_world as dbs_fusion_world
import card_games.grand_archive as grand_archive
import card_games.one_piece as one_piece
import card_games.lorcana as lorcana
import card_games.city_of_heroes as city_of_heroes
import card_games.daemon_dice as daemon_dice
import card_games.dragon_dice as dragon_dice
import card_games.star_trek_second_edition as star_trek_second_edition
import card_games.star_trek_first_edition as star_trek_first_edition
import card_games.tribbles as tribbles
import card_games.star_wars_unlimited as star_wars_unlimited
import card_games.magic_gathering as magic_gathering
import card_games.l5r as l5r

if os.getcwd().endswith('card-minis-boardgames'):
    sys.path.append('.')
    from utils.output_utils import double_print
    in_file = open("card_games/DB/NewCardGames.txt", encoding="UTF-8")
else:
    sys.path.append('.')
    from utils.output_utils import double_print
    in_file = open("DB/NewCardGames.txt", encoding="UTF-8")

#print("\033[96mTest.\033[0m")

started_games = [anachronism, daemon_dice, dragon_dice, star_wars_unlimited,
    star_trek_second_edition, tribbles, city_of_heroes, wyvern, dbs_fusion_world, grand_archive,
    lorcana, one_piece, magic_gathering, l5r, star_trek_first_edition]

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
    total_string = f"Totaling {len(game_data) - 1} games, owning {TOTAL_HAVE} out of " + \
        f"{TOTAL_MAX} cards/dice ({total_percentage:.2f} percent)"
    double_print(total_string, out_file_h)
    lowest_game_percentage = game_data[0][1]*100/game_data[0][2]
    lowest_game_string = f"Lowest game is {game_data[0][0]} at {lowest_game_percentage:.2f} " + \
        f"percent ({game_data[0][1]} / {game_data[0][2]})"
    double_print(lowest_game_string, out_file_h)

    double_print("\nFive Lowest Games (by percentage):", out_file_h)
    for game_info in game_data[:5]:
        info_n, info_h, info_t = game_info
        info_p = info_h/info_t
        pt_str = f"- {info_n}: {100 * info_p:.2f} ({info_h}/{info_t})"
        double_print(pt_str, out_file_h)

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

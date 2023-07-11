#!/usr/bin/python3

import os, sys

import DaemonDice, DragonDice

#print("\033[96mTest.\033[0m")

total_have = 0
total_max = 0
new_games_started = 1
game_data = []

started_games = [DaemonDice, DragonDice]

if os.getcwd().endswith('card-minis-boardgames'):
    in_file = open("card_games/DB/NewCardGames.txt")
else:
    in_file = open("DB/NewCardGames.txt")
other_games = in_file.readlines()
in_file.close()
other_games = [line.strip() for line in other_games]

new_games_count = len(other_games) + new_games_started

for game in started_games:
    total_have += game.total_own
    total_max += game.total_max
    game_data.append((game.GAME_NAME, game.total_own, game.total_max))

game_data.append(("New Game", new_games_started + 1, new_games_count+1))
game_data = sorted(game_data, key=lambda x:(x[1]/x[2], -1 * (x[2] - x[1])))

if __name__ == "__main__":
    if os.getcwd().endswith('card-minis-boardgames'):
        out_file_h = open("card_games/output/CCGSummaryOut.txt", 'w')
    else:
        out_file_h = open("output/CCGSummaryOut.txt", 'w')
    total_string = "Totaling %d games, owning %d out of %d (%.2f percent)" % (len(game_data) - 1, total_have, total_max, total_have * 100 /total_max)
    print(total_string)
    out_file_h.write(total_string + "\n")
    lowest_game_string = "Lowest game is %s at %.2f percent (%d / %d)" % (game_data[0][0], (game_data[0][1]*100/game_data[0][2]), game_data[0][1], game_data[0][2])
    print(lowest_game_string)
    out_file_h.write(lowest_game_string + "\n")
    next_lowest_string = "- (Next lowest game is %.2f percent)" % (game_data[1][1] * 100 / game_data[1][2])
    print(next_lowest_string)
    out_file_h.write(next_lowest_string + "\n")

    out_file_h.close()
    if not os.getcwd().endswith('card-minis-boardgames'):
        input("Press enter to continue...")

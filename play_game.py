import random

import risk_game
from country import Country
from data import targets, continents, continent_bonus
from risk_game import RiskGame


if __name__ == "__main__":
    result_list = list()
    game = RiskGame(4)

    # pick countries
    for i in range(0, 42):
        player_id = i % game.amount_players  # 3 is amount of players
        result = game.pick_countries(player_id)
        print("Picked country: " + str(result))
        game.countries[result].owner = player_id
        game.countries[result].amount_soldiers = 1

    # pick placement
    for i in range(0, 84):
        player_id = i % game.amount_players  # 3 is amount of players
        result = game.pick_placement(player_id)
        print("Placed reinforcement: " + str(result))
        game.countries[result].amount_soldiers += 1
        game.country_worth[result] = game.get_worth(result, player_id)

    # game.print_board()

    # make steppable by player/turn
    turn_count = 0
    all_country_one_owner = False
    did_move_last_turn = []
    for player_id in range(0, game.amount_players):
        did_move_last_turn.insert(player_id, False)

    while not all_country_one_owner:
        turn_count += 1
        print("TURN: " + str(turn_count))

        for player_id in range(0, game.amount_players):
            owned_countries = game.get_owned_country_ids(player_id)
            if len(owned_countries) > 0:
                reinforcements = game.get_reinforcements(player_id)

                while reinforcements > 0:  # placement
                    result = game.pick_placement(player_id)
                    # print("Placed reinforcement: " + str(result))
                    game.countries[result].amount_soldiers += 1
                    game.country_worth[result] = game.get_worth(result, player_id)
                    reinforcements -= 1

                amount_moves = game.get_amount_moves(player_id)
                amount_moves = max(amount_moves, 5)
                for move_count in range(0, amount_moves):
                    print("TURN: " + str(turn_count) + "\t\tPLAYER: " + str(player_id) + "\t\tMOVE: " + str(move_count))
                    possible_moves = []
                    for country_id in owned_countries:
                        for target_id in game.countries[country_id].targets:
                            if game.countries[target_id].owner != player_id:
                                if game.countries[country_id].amount_soldiers > 2:
                                    succes_chance = game.countries[country_id].amount_soldiers / 99 * 100 * 0.42
                                    possible_move = {"source": country_id, "target": target_id, "succes_chance": succes_chance}
                                    possible_moves.append(possible_move)

                    possible_moves.sort(reverse=True, key=game.chance_sort)
                    print(possible_moves)

                    if len(possible_moves) > 0:
                        move = random.randint(0, len(possible_moves)) - 1
                        source_id = possible_moves[move]["source"]
                        target_id = possible_moves[move]["target"]
                        print(possible_moves[move])
                        game.do_move(source_id, target_id, game.countries[source_id].amount_soldiers - 2)
                        did_move_last_turn[player_id] = True

        for player_id in range(0, game.amount_players):
            if len(game.get_owned_country_ids(player_id)) == 42:
                print("PLAYER " + str(player_id) + " WON !")
                all_country_one_owner = True

        string = ""
        for player_id in range(0, game.amount_players):
           string += "player [" + str(player_id) + "]:" + str(len(game.get_owned_country_ids(player_id))) + "\t"
        print("\n\n" + string)

    # game.print_board()

    # for entry_id in range(0, 42):
    # print(str(entry_id) + " - " + str(result_list.count(entry_id)))

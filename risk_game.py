import random
import sys

from country import Country
from data import targets, continents, continent_bonus


class RiskGame:
    def __init__(self, amount_players):
        self.country_worth = []
        self.amount_players = amount_players

        self.countries = []
        for i in range(0, 42):
            owner = -1
            amount_soldiers = 0

            """if i == 38 or i == 39 or i == 40:
                owner = 1
            elif i == 41:
                owner = -1
            """

            self.countries.insert(i, Country(i, owner, amount_soldiers))

    def get_owned_country_ids(self, player_id):
        owned_countries = []
        for country_id in range(0, 42):
            if self.countries[country_id].owner == player_id:
                owned_countries.append(country_id)
        return owned_countries

    def get_maxes(self):
        max_int_worth_cont = 0
        max_int_worth_target = 0
        for i in range(0, 42):
            for c in range(0, len(continents)):
                if i in continents[c] and len(continents[c]) > max_int_worth_cont:
                    max_int_worth_cont = len(continents[c])
            for t in range(0, len(targets)):
                if i in targets[t] and len(targets[t]) > max_int_worth_target:
                    max_int_worth_target = len(targets[t])

        # print("cont:" + str(max_int_worth_cont) + "\ttarget:" + str(max_int_worth_target))
        return max_int_worth_cont, max_int_worth_target

    @staticmethod
    def worth_sort(e):
        return e["worth"]

    @staticmethod
    def chance_sort(e):
        return e["succes_chance"]

    def print_board(self):
        for i in range(0, 42):
            current_country_worth = self.get_worth(i, self.countries[i].owner)
            print(self.countries[i])
            print("Id:" + str(i) + " intrinsic worth is \t" + str(current_country_worth["int"]))
            print("Id:" + str(i) + " continent worth is  \t" + str(current_country_worth["con"]))
            print("Id:" + str(i) + " defence worth is  \t\t" + str(current_country_worth["def"]))
            total_worth = (current_country_worth["int"] + current_country_worth["con"] + current_country_worth["def"])
            print("Id:" + str(i) + " total worth is \t\t" + str(total_worth) + "\n")

    def get_worth(self, country_id, player_id):
        max_int_worth_cont, max_int_worth_target = self.get_maxes()

        target_own_count = 0
        for j in range(0, len(targets[country_id])):
            if self.countries[targets[country_id][j]].owner == player_id:
                target_own_count += 1
        defence_worth = target_own_count / len(targets[country_id]) * 100
        defence_worth += self.countries[country_id].amount_soldiers * 10

        continent_worth = 0
        for j in range(0, len(continents)):
            if country_id in continents[j]:
                continent_worth += continent_bonus[j]

                continent_own_count = 0
                continent_len = len(continents[j])
                for k in range(0, continent_len):
                    if self.countries[continents[j][k]].owner == player_id:
                        continent_own_count += 1
                continent_worth = continent_own_count / continent_len * 100

                if continent_own_count == continent_len - 1 and self.countries[country_id].owner == -1:
                    continent_worth += 250
                    # print("bonus worth -1")
                elif continent_own_count == continent_len - 2 and self.countries[country_id].owner == -1:
                    continent_worth += 100
                    #  print("bonus worth -2")

        # calculate intrinsic worth
        intrinsic_worth = 0
        for j in range(0, len(continents)):
            if country_id in continents[j]:
                intrinsic_worth_continents = len(continents[j]) / 8 * 100
                intrinsic_worth_targets = (max_int_worth_target - len(targets[country_id])) / 8 * 100
                intrinsic_worth = (intrinsic_worth_continents + intrinsic_worth_targets) / 2

        return {"int": intrinsic_worth, "con": continent_worth, "def": defence_worth}

    def pick_countries(self, player_id):
        # Adjust for non picked counries

        total_worth_all_countries = 0
        countries_sorted = list()
        for l in range(0, 42):
            self.country_worth.insert(l, self.get_worth(l, player_id))
            total_worth = (self.country_worth[l]["int"] + self.country_worth[l]["con"] + self.country_worth[l]["def"])
            countries_sorted.append({"id": l, "owner": self.countries[l].owner, "worth": total_worth});
            # print("Id:" + str(i) + " total worth is \t\t" + str(total_worth) + "\n")

        total_worth_top_10_countries = 0
        countries_sorted.sort(key=self.worth_sort, reverse=True)
        for l in range(0, 10):
            if countries_sorted[l]["owner"] == -1:
                total_worth_top_10_countries += countries_sorted[l]['worth']

        # if no complete continent
        # If no block continent other player
        # print(total_worth_top_10_countries)
        can_block, can_block_id = self.block_check()
        # print("blckchk: (" + str(can_block) +","+ str(can_block_id) +")")
        if can_block:
            if self.countries[can_block_id].owner == -1:
                print("blocked" + str(can_block_id))
                return can_block_id
        else:
            result = random.randint(0, int(total_worth_top_10_countries / 2))
            for l in range(0, 42):
                if countries_sorted[l]["owner"] == -1:
                    result -= countries_sorted[l]["worth"]
                    # print(str(l) + " with id " + str(countries_sorted[l]["id"]) + " result : " + str(result))

                if 1 > result:
                    if self.countries[countries_sorted[l]["id"]].owner == -1:
                        return countries_sorted[l]["id"]

    def block_check(self):
        continent_owners = []
        for i in range(0, len(continents)):
            continent_owners.append(i)
            continents_len = len(continents[i])
            continent_owners[i] = []
            for _ in range(0, self.amount_players):
                continent_owners[i].append(0)

            for j in range(0, len(continents[i])):
                # print(continents[i][j])
                if self.countries[continents[i][j]].owner != -1:
                    continent_owners[i][self.countries[continents[i][j]].owner] += 1

        # print("conown:" + str(continent_owners))
        almost_complete_continent_country_id = []
        for i in range(0, len(continent_owners)):
            for j in range(0, len(continent_owners[i])):
                if continent_owners[i][j] == len(continents[i]) - 1 or continent_owners[i][j] == len(continents[i]) - 2:
                    for country_id in continents[i]:
                        if self.countries[country_id].owner == -1:
                            return True, country_id

        return False, -1

    def pick_placement(self, player_id):
        worth_array = []
        for country_id in range(0, 42):
            worth_array.insert(country_id, self.get_worth(country_id, player_id))

        saved_id = -1
        lowest = 200000
        for country_id in range(0, 42):
            if worth_array[country_id]["def"] < lowest and self.countries[country_id].owner == player_id:
                lowest = worth_array[country_id]["def"]
                saved_id = country_id
        return saved_id

    def get_reinforcements(self, player_id):
        reinforcements = 0
        for continent_id in range(0, len(continents)):
            all_owned = True
            for country_id in continents[continent_id]:
                if self.countries[country_id] != player_id:
                    all_owned = False
                    break
            if all_owned:
                reinforcements += continent_bonus[continent_id]

        reinforcements = len(self.get_owned_country_ids(player_id)) / 2
        return reinforcements

    def do_move(self, source_id, target_id, amount_soldiers):
        deaths_source = 0
        deaths_target = 0
        amount_soldiers_target = self.countries[target_id].amount_soldiers
        while amount_soldiers != deaths_source and amount_soldiers_target != deaths_target:
            dice_defencer = random.randint(1, 30)
            dice_attacker = random.randint(1, 29)

            if dice_defencer > dice_attacker or dice_defencer == dice_attacker:
                deaths_source += 1
            else:
                deaths_target += 1

            if amount_soldiers_target == deaths_target:
                self.countries[target_id].owner = self.countries[source_id].owner
                self.countries[target_id].amount_soldiers = amount_soldiers
            self.countries[source_id].amount_soldiers -= amount_soldiers

    def get_amount_moves(self, player_id):
        amount_units = 0
        for country_id in range(0, 42):
            if self.countries[country_id].owner == player_id:
                amount_units += self.countries[country_id].amount_soldiers

        return 1 + round(amount_units / 5)

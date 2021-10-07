import random


def get_maxes():
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


targets = [
    [1, 32],
    [0, 2, 5, 6],
    [1, 3, 4, 7],
    [2, 4, 7],
    [2, 3, 4, 5],
    [1, 4, 6, 8],
    [1, 5, 8],
    [2, 3, 14],
    [6, 5, 9, 10],
    [5, 8, 10],
    [9, 10, 12, 11],
    [10, 12, 21],
    [10, 11, 41],
    [14, 16, 17, 20],
    [7, 13, 15],
    [13, 14, 16, 18],
    [13, 14, 15, 17, 29, 18],
    [13, 16, 19, 20],
    [15, 16, 30, 31],
    [16, 17, 26, 27, 29, 30],
    [13, 17, 21, 22, 26],
    [11, 20, 22, 23],
    [20, 21, 23, 26, 28],
    [21, 22, 24, 25],
    [23, 25],
    [23, 24],
    [19, 20, 22, 27, 28],
    [19, 26, 27, 28, 29],
    [22, 26, 27, 29],
    [27, 28, 30, 34],
    [18, 19, 29, 31],
    [18, 30, 32, 33],
    [0, 31, 33, 36],
    [29, 30, 31, 32, 34, 35, 36, 37],
    [29, 33, 35],
    [33, 34, 37, 38],
    [32, 33, 37],
    [33, 35, 36, 38, 39],
    [35, 37, 39, 40],
    [37, 38, 40],
    [38, 39, 41],
    [40, 12]
]

# Refactor

continents = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [8, 9, 10, 11, 12],
    [13, 14, 15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24, 25],
    [26, 27, 28, 29, 30],
    [31, 32, 33, 34, 35, 36, 37],
    [38, 39, 40, 41]
]

continent_bonus = [
    4, 2, 3, 3, 2, 3, 2
]


class PickCountry:
    def __init__(self):
        pass


class Move:
    def __init__(self, origin_id, target_id, amount_soldiers):
        self.origin_id = origin_id
        self.target_id = target_id
        self.amount_soldiers = amount_soldiers


class Place:
    def __init__(self, country_id):
        self.country_id = country_id


class Pick:
    def __init__(self, country_id):
        self.country_id = country_id


class Country:
    def __init__(self, id, owner, amount_soldiers):
        self.id = id
        self.owner = owner
        self.amount_soldiers = amount_soldiers
        self.targets = targets[id]

    def __str__(self):
        targets_string = ""

        for i in range(0, len(self.targets)):
            targets_string += str(self.targets[i]) + ", "

        return str(self.id) + "\tOwner: " + str(self.owner) + \
               "\tAmount soldiers: " + str(self.amount_soldiers) + \
               "\tTargets: " + targets_string


class RiskGame:
    def __init__(self):
        self.amount_players = 3

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

    @staticmethod
    def my_sort(e):
        return e["worth"]

    def print_board(self):
        for i in range(0, 42):
            self.country_worth = self.get_worth(self.countries[i].owner)
            print(self.countries[i])
            print("Id:" + str(i) + " continent worth is  \t" + str(self.country_worth[i][1]))
            print("Id:" + str(i) + " defence worth is  \t\t" + str(self.country_worth[i][2]))
            print("Id:" + str(i) + " intrinsic worth is \t" + str(self.country_worth[i][0]))
            total_worth = (self.country_worth[i][0] + self.country_worth[i][1] + self.country_worth[i][2])
            print("Id:" + str(i) + " total worth is \t\t" + str(total_worth) + "\n")

    def get_worth(self, player_id):
        max_int_worth_cont, max_int_worth_target = get_maxes()

        country_worth = list()
        for country_id in range(0, len(targets)):
            target_own_count = 0
            for j in range(0, len(targets[country_id])):
                if self.countries[targets[country_id][j]].owner == player_id:
                    target_own_count += 1
            defence_worth = target_own_count / len(targets[country_id]) * 100

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

            country_worth.append([intrinsic_worth, continent_worth, defence_worth])
        return country_worth

    def pick_countries(self, player_id):
        # Adjust for non picked counries

        total_worth_all_countries = 0
        countries_sorted = list()
        for l in range(0, 42):
            total_worth = (self.country_worth[l][0] + self.country_worth[l][1] + self.country_worth[l][2])
            countries_sorted.append({"id": l, "owner": self.countries[l].owner, "worth": total_worth});
            # print("Id:" + str(i) + " total worth is \t\t" + str(total_worth) + "\n")

        total_worth_top_10_countries = 0
        countries_sorted.sort(key=self.my_sort, reverse=True)
        for l in range(0, 10):
            if countries_sorted[l]["owner"] == -1:
                total_worth_top_10_countries += countries_sorted[l]['worth']

        # if no complete continent
        # If no block continent other player
        # print(total_worth_top_10_countries)
        result = random.randint(0, int(total_worth_top_10_countries / 2))
        for l in range(0, 42):
            if countries_sorted[l]["owner"] == -1:
                result -= countries_sorted[l]["worth"]
                # print(str(l) + " with id " + str(countries_sorted[l]["id"]) + " result : " + str(result))

            if 1 > result:
                if self.countries[countries_sorted[l]["id"]].owner == -1:
                    print("Pick: " + str(countries_sorted[l]["id"]))
                    return countries_sorted[l]["id"]

    def pick_move(self):
        pass


if __name__ == "__main__":
    result_list = list()
    game = RiskGame()
    for i in range(0, 42):
        player_id = i % game.amount_players  # 3 is amount of players
        game.country_worth = game.get_worth(player_id)
        result = game.pick_countries(player_id)
        game.countries[result].owner = player_id
        print(game.countries[result].owner)
        result_list.append(result)

    game.print_board()

    for entry_id in range(0, 42):
        print(str(entry_id) + " - " + str(result_list.count(entry_id)))

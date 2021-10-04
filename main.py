import random

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
            owner = random.randint(0, self.amount_players)
            amount_soldiers = random.randint(0, 10)

            self.countries.insert(i, Country(i, 1, amount_soldiers))

        self.country_worth = self.get_worth(2)

    def print_board(self):
        for i in range(0, 42):
            print(self.countries[i])
            print("Id:" + str(i) + " continent worth is  \t" + str(self.country_worth[i][0]))
            print("Id:" + str(i) + " target worth is  \t\t" + str(self.country_worth[i][1]))
            print("Id:" + str(i) + " intrinsic worth is \t" + str(self.country_worth[i][2]))
            total_worth = (self.country_worth[i][0] + self.country_worth[i][1] + self.country_worth[i][2]) / 3
            print("Id:" + str(i) + " total worth is \t\t" + str(total_worth) + "\n")

    def get_worth(self, player_id):
        country_worth = list()
        for i in range(0, len(targets)):
            target_own_count = 0
            for j in range(0, len(targets[i])):
                if self.countries[targets[i][j]].owner == player_id:
                    target_own_count += 1
            target_worth = target_own_count / len(targets[i]) * 100

            continent_worth = 0
            for j in range(0, len(continents)):
                if i in continents[j]:
                    continent_worth += continent_bonus[j]

                    continent_own_count = 0
                    continent_len = len(continents[j])
                    for k in range(0, continent_len):
                        if self.countries[continents[j][k]].owner == player_id:
                            continent_own_count += 1
                    continent_worth = continent_own_count / continent_len * 100

            # calculate intrinsic worth
            intrinsic_worth = 0
            for j in range(0, len(continents)):
                if i in continents[j]:
                    intrinsic_worth = len(continents[j]) / continent_bonus[j]
                    intrinsic_worth += len(targets[i]) / 2
                    intrinsic_worth = intrinsic_worth / 6.333333333333334 * 100

            country_worth.append([intrinsic_worth, continent_worth, target_worth])
        return country_worth

    def pick_countries(self):
        countries_picked = list()

        while len(countries_picked) != 42:
            max_value = 0
            for i in range(0, self.amount_players):
                country_worth = self.get_worth(i)
                for j in range(0, 42):
                    if country_worth[j][0] > max_value and j not in countries_picked:
                        max_value = country_worth[j][0]

            possible_picks = list()
            for i in range(0, 42):
                if country_worth[i][0] == max_value and i not in countries_picked:
                    print("picked: " + str(i))
                    possible_picks.append(i)
                    countries_picked.append(i)

            print(possible_picks)

if __name__ == "__main__":
    game = RiskGame()
    game.print_board()
    game.pick_countries()

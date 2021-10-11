from data import targets


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

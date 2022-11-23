from random import randint


class Bank:
    default_value_sum = 212 * (10 ** 6)
    default_investors_count = 2 * (10 ** 3)
    banks = []

    def __init__(self):
        self.investors = []
        s = Bank.default_value_sum
        prev_i = 0
        for i in range(Bank.default_investors_count):
            i = prev_i + round(randint(round(1), round(7)) / 10000, 4)
            newval = round(s * (i - prev_i), 2)
            self.investors.append(Investor(newval))
            s -= newval
            prev_i = round(i, 4)


class Investor:
    def __init__(self, depo):
        self.deposit = depo

    def __repr__(self):
        return str(self.deposit)

    def __ge__(self, other):
        return self.deposit >= other.deposit

    def __lt__(self, other):
        return self.deposit < other.deposit

    def __eq__(self, other):
        return self.deposit == other.deposit

    def addDepo(self, depo):
        self.deposit += depo


def initWorld():
    Bank.banks = []
    for i in range(100):
        b = Bank()
        Bank.banks.append(b)
    for b in Bank.banks:
        b.investors = sorted(b.investors)
        s = 0
        for i in (b.investors):
            s += i.deposit
        b.investors[0].addDepo((Bank.default_value_sum - s) / 3)
        b.investors[1].addDepo((Bank.default_value_sum - s) / 3)
        b.investors[2].addDepo((Bank.default_value_sum - s) / 3)
        b.investors = sorted(b.investors, reverse = True)
        print(min(b.investors))


initWorld()
print(1)

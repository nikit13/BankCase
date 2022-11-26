from random import randint


class CentralBank:
    banks = []
    bankruptBanks = []
    bankruptInvestors = []
    droppedInvestors = []
    global_awareness = 1
    inflation = 0.1

    @staticmethod
    def count_gains():
        for i in CentralBank.bankruptInvestors:
            pass
        for i in CentralBank.bankruptBanks:
            pass
        for i in CentralBank.droppedInvestors:
            pass
        for i in CentralBank.banks:
            pass


class Bank:
    default_value_sum = 212 * (10 ** 6)
    default_investors_count = 2 * (10 ** 3)

    def __init__(self):
        self.investors = []
        s = Bank.default_value_sum
        self.reserve = s
        self.rate_on_depo = CentralBank.inflation
        self.gain = 0
        prev_i = 0
        for i in range(Bank.default_investors_count):
            i = prev_i + round(randint(round(1), round(7)) / 10000, 4)
            newval = round(s * (i - prev_i), 2)
            self.investors.append(Investor(newval))
            s -= newval
            prev_i = round(i, 4)

    def dropDepos(self):
        for i, inv in enumerate(self.investors):
            inv.awareness = inv.awareness_count(self)
            if inv.awareness > randint(50, 100):

                self.reserve -= inv.deposit
                inv.gain = inv.deposit
                inv.deposit = 0
                CentralBank.droppedInvestors.append(self.investors[i])

                self.investors.pop(i)
                if self.reserve < 0:
                    self.bankrupt()
                    return True
        return False

    def bankrupt(self):
        for i, inv in enumerate(self.investors):
            inv.gain = -100
            CentralBank.bankruptInvestors.append(self.investors[i])
        CentralBank.bankruptBanks.append(self)
        return True


class Investor:
    def __init__(self, depo):
        self.deposit = depo
        self.awareness = 1
        self.gain = 0

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

    def awareness_count(self, bank):
        return self.deposit / (
                    Bank.default_value_sum / Bank.default_investors_count) * CentralBank.inflation * CentralBank.global_awareness / bank.rate_on_depo


def initWorld():
    Bank.banks = []
    for i in range(100):
        b = Bank()
        CentralBank.banks.append(b)
    for b in CentralBank.banks:
        b.investors = sorted(b.investors)
        s = 0
        for i in b.investors:
            s += i.deposit
        b.investors[0].addDepo((Bank.default_value_sum - s) / 3)
        b.investors[1].addDepo((Bank.default_value_sum - s) / 3)
        b.investors[2].addDepo((Bank.default_value_sum - s) / 3)
        b.investors = sorted(b.investors, reverse = True)
        print(min(b.investors))


initWorld()
print(1)

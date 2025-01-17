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
        investors_gain = 0
        banks_gain = 0
        for i in CentralBank.bankruptInvestors:
            investors_gain += i.gain
        for i in CentralBank.bankruptBanks:
            banks_gain += i.gain
        for i in CentralBank.droppedInvestors:
            investors_gain += i.gain
        for i in CentralBank.banks:
            banks_gain += i.reserve + i.investments
        return banks_gain, investors_gain


class Bank:
    default_value_sum = 212 * (10 ** 6)
    default_investors_count = 2 * (10 ** 3)

    def __init__(self, ror):
        self.term_sur = 0
        self.investors = []
        s = Bank.default_value_sum
        self.rate_on_reserves = ror
        self.reserve = s * ror
        self.investments = s * (1 - ror)
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
                self.investors[i].gain = inv.deposit
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
        b = Bank(randint(0, 100) / 100)
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
        # print(min(b.investors))


initWorld()  # инициализация
for term in range(10):
    CentralBank.inflation += 0.1  # рост инфляции каждый "цикл"
    for q, bank in enumerate(CentralBank.banks):
        CentralBank.banks[q].term_sur += 1
        if bank.dropDepos():  # если банк обанкротился
            for inv in bank.investors:
                CentralBank.banks[q].gain -= inv.deposit
            CentralBank.banks.pop(q)
        else:
            for i, inv in enumerate(bank.investors):
                CentralBank.banks[q].reserve -= inv.deposit * bank.rate_on_depo  # выплачиваем проценты вкладчикам
                CentralBank.banks[q].investors[i].deposit *= (bank.rate_on_depo + 1)
            CentralBank.banks[q].investments *= (CentralBank.inflation * 2)  # TODO не должно быть просто в 2 раза выше
            s = CentralBank.banks[q].reserve + CentralBank.banks[q].investments  # все активы банка
            CentralBank.banks[q].reserve, CentralBank.banks[q].investments = s * bank.rate_on_reserves, s * (
                    1 - bank.rate_on_reserves)  # пересчитываем капитал банка (собрали все деньги и поделили по ставке)

print("gains", CentralBank.count_gains())
for bank in CentralBank.banks:
    print(bank.rate_on_reserves, len(bank.investors))

print(len(CentralBank.banks))

for bank in CentralBank.bankruptBanks:
    print(bank.rate_on_reserves, len(bank.investors))

print(len(CentralBank.bankruptBanks))

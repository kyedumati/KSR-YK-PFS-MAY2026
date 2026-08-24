class BankAccount:
    def __init__(self, holder, balance=0):
        self.holder = holder
        self._balance = float(balance)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount

    def get_balance(self):
        return self.__balance

    def set_balance(self, amount):
        self.__balance = amount

class SavingAccount(BankAccount):
    def __init__(self, holder, balance=0, rate=0.04):
        super().__init__(holder, balance)
        self.rate = float(rate)

    def apply_interest(self):
        self.deposit(self.__balance * self.rate)

    def __str__(self):
        return f"Saving: {self.holder}, {self.__balance}, {self.rate}"


account = BankAccount("kasi", 1000)
print(account)
print(account.get_balance())
account.__balance = 100 # this will not do any operation and prevents accidental modifications
print(account.get_balance()) # tbis is the only way to check balance

savings_account = SavingAccount("kasi", 1000)
savings_account.apply_interest()
print(savings_account)
savings_account.__balance = -10 # im manipulating account balance being an outsider, this shouldnt be allowed
print(savings_account)
print(savings_account.__balance)

# print(savings_account.get_balance())

saving

class AccountUnderScore:
    def __init__(self, name, balance):
        self.name = name
        self._balance = balance   # convention only

    @property
    def balance(self):  # looks like attribute, runs method when someone tried to access the data member
        return self._balance


class AccountDoubleUnderscore:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

u = AccountUnderScore("Kasi", 100)
d = AccountDoubleUnderscore("Naveen", 200)
print("Balance of u is:", u.balance)
print(u._balance)
u._balance = -50 # it is dangeours operation
print("Balance after update u is:", u._balance)

u = FaceBookSignupForm("name", "") # initilising the data we are setting the data, if we want to get the data

d.__balance = -50
# print("Balance after update u is:", d._balance)
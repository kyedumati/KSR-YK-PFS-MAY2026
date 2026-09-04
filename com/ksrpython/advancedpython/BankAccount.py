class BankAccount:  # parent class
    def __init__(self, holder_name, email, mobile_no, balance=0 ):
        self.holder_name = holder_name
        self.email = email
        self.mobile_no = mobile_no
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            print("Invalid amount.")

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
            else:
                print("Insufficient funds.")
        else:
            print("Invalid amount.")

    def get_balance(self):
        return self.balance


class SavingsAccount(BankAccount): # child class  # SavingsAccount is a BankAccount
    def __init__(self, holder_name, email, mobile_no, aadhar, balance=0):  # duplicate code
        # super().__init__(holder_name, email, mobile_no)
        super().__init__(holder_name, email, mobile_no, balance) # super class constructor is being called from child class, that statement should be always at first
        self.aadhar = aadhar

    def apply_interest(self):
        self.deposit(self.balance * 0.2)


class CreditAccount(BankAccount):
    def __init__(self, holder_name, email, mobile_no, balance=0):
        super().__init__(holder_name, email, mobile_no, balance)

    def apply_interest(self): # negative interest
        self.deposit(-self.balance * 0.2)

    def generate_bill(self):
        print("Generating bill...")


# bank_account = BankAccount("Nani", "test@gmail.com", "123456")
# print("Current balance: ", bank_account.get_balance())
# bank_account.deposit(2000)
# print("Current balance after depositr: ", bank_account.get_balance())

# bank_account = BankAccount("Nani", "test@gmail.com", "123456")
saving_account = SavingsAccount("kasi yedumati", "kasi@gmail.com", "6302193992", "123456789")
# deposit balance
saving_account.deposit(2000)
saving_account.apply_interest()
print("Current balance: ", saving_account.get_balance())

# "/Users/kasiy/Desktop/KSR_Trainings/WORKSPACE/KSR-YK-PFS-MAY2026/student_info.csv"
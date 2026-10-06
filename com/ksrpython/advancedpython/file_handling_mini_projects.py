# # Create a program to take all the expenses(category, item, price, date) as an input and then save those expendes to csv file
# # Write methods also to calculate final expenses catogory wise
# #ex: category : food, healthcare, entertainment
# # IteM: biryani, op and medicine bill for fever, movies/games

# 1. View All Expenses
# 2. Add Expense
# 3. Total Expenses   --> read the csv files, get price from that and create a temp total variable and sum it
# 4. Category-wise Report  --> output should
# 5. Highest Expense  --> which category you are spening more amount and whats the amount: Ex: groceries, 1200
# 6. Lowest Expense  --> entertainment: 350
# 7. Search by Category --> Input: food: output: should list all the items in that category only
# 8. Payment Mode Report -->
# 9. Exit

from csv import *
import csv
import os

from logging_config import get_logger
# import logging

logger = get_logger(__name__)

# logging.basicConfig(filename='expenses_logfile.log', filemode="a", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")



class Expense: # this is to hold all the properties of the expenses
    def __init__(self, date, category, description, amount, payment_mode):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.payment_mode = payment_mode

    def __str__(self):
        return f"Date: {self.date} \n Caregory:{self.category} \n Description:{self.description} \n Amount:{self.amount} \n PaymentMode:{self.payment_mode}"


class ExpenseManager:
    def __init__(self, filename):
        self.filename = filename
        self.expenses = [] # empty expenses
        self.create_file()

    def create_file(self):
        if not os.path.exists(self.filename):
            logger.debug("File doesn't exist, im creating new file") # DEBUG, application flow
            with open(self.filename, "w") as file:
                writer_obj = DictWriter(file, fieldnames=["date", "category", "description", "amount", "payment_mode"])
                writer_obj.writeheader()
                # writer = csv.writer(file)
                # writer.writ(["date", "category", "description", "amount", "payment_mode"])

    def view_expenses(self):
        logger.info("VIEW EXPENSES VIEW")
        self.expenses = []
        try:
            with open(self.filename, "r") as file:
                reader = DictReader(file)
                for row in reader:
                    expense = Expense(row.get("date"), row.get("category"), row.get("description"), row.get("amount"),row.get("payment_mode"))
                    self.expenses.append(expense)
        except FileNotFoundError as e:
            logger.error("File doesn't exist, im creating new file", e)
        else:
            print("ALL EXPENSES VIEW")
            for item in self.expenses:
                print("=====================")
                print(item)
                print("=====================")

    def add_expense(self, expense:Expense):
        # message = "Adding expense {0}, {1}, {2}".format(expense.date, expense.category, expense.description)
        # message = f"Adding expense category={category}, description={description}, amount={amount}, payment_mode={payment_mode}"
        message = "Adding expense category={category}, description={description}, amount={amount}, payment_mode={payment_mode}".format(category=expense.category, description=expense.description, amount=expense.amount, payment_mode=expense.payment_mode)

        logger.info(message)
        self.expenses.append(expense)

        # write to the file
        with open(self.filename, "a") as file:
            writer = csv.writer(file)
            writer.writerow([
                expense.date,
                expense.category,
                expense.description,
                expense.amount,
                expense.payment_mode
            ])
        logger.info("Successfully added expense") # info


if __name__ == "__main__":
    manager = ExpenseManager("expenses.csv")
    while True:
        print("=========MONTHLY EXPENSES TRACKER============")
        print("1. View All Expenses")
        print("2. Add expense")
        print("3. Total Expenses")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            manager.view_expenses()
        elif choice == 2:
            date = input("Enter your date: ")
            category = input("Enter your category: ")
            description = input("Enter your description: ")
            amount = input("Enter your amount: ")
            payment_mode = input("Enter your payment mode: ")
            expense = Expense(date, category, description, amount, payment_mode)
            manager.add_expense(expense)












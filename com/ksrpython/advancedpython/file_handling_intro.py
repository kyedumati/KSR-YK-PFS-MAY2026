# with open("test.txt", "a") as f:
#     f.write("Hello World\n")
#     f.write("Going to office\n")

expense_type = input("What is the expense type?")
amount = input("What is the amount?")

file_location = "data/expense.txt"
f = open(file_location, "a") # we are trying to open test.txt file in a append mode
# f.write("2026-09-07 | restaurant bill | 1200\n")
f.write("2026-09-07 | "+ expense_type + " " + amount+ "\n")
# f.close()
f.close() # closing the resource is highlt recommned, otherwise we will get corrupted file or unsaved data
print("Your expenses are added successfully")

# read the file
# try:
#     bank_statement_location = "bank_statement.csv"
#     f = open(bank_statement_location, "r")
# except FileNotFoundError as err:
#     print("File not found")
# else:
#     f.write("Add dummy write")
# finally:
#     f.close()
bank_statement_location = "expense.txt"
with open(bank_statement_location, "r") as f:
    # print(f.readlines()) # ['2026-09-07 | restaurant 1300\n', '2026-09-07 | tea 320\n', '2026-09-07 | Milk 100\n', '2026-09-07 | Milk 120\n', '2026-09-07 | tea 12\n', '2026-09-07 | ta 12\n', '2026-09-07 | tea 12\n']
    for line in f.readlines():
        print(line)
# file is already closed


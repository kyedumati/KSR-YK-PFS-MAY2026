# we have a module csv
from csv import DictReader, DictWriter
# we have csv.writer , csv.reader functions to perform operations on the data
file_loc = "data/monthly_expenses.csv"
total_expenses = 0
#
with open(file_loc, "r", encoding="utf-8") as f:
    for row in DictReader(f):
        print(row.get("price"))
        total_expenses += int(row.get("price"))
print(total_expenses)

# rows = [
#     {"category": "food", "price":"120", "ItemName": "Tea", "date": "2026-09-08" },
#     {"category": "travel", "ItemName": "Pondicherry", "date": "2026-09-05", "price":"35000"}
# ]
#
# with open(file_loc, "a") as csvfile:
#     writer = DictWriter(csvfile, fieldnames=["category", "price", "ItemName", "date"])
#     # writer.writeheader()
#     writer.writerows(rows) # writing multipple rows to the csv file at a time
#     # writer.writerow(rows[0]) #wrfiting a single row to the csv files








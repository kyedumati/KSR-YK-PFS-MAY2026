students = ["pooja", "chandu", "varshith", "naga", "divya", "bhuvan"]
#I want to find naga in my students
# for student in students:
#     if student == "naga":
#         print("Naga is available in the class")
#         break

# write a program to identify and validate if any of my cart items are more than 500 rupees
# cart_items = [{
#  "item_name": "tshirt",
#     "item_price": "499"
# }, {"item_name": "shirt", "item_price": "1499" }]

cart_amounts = [10,20,500,600,20,40]
for price in cart_amounts:
    if price > 500:
        print("its more than my budget, I dont want continue billing here")
        break
    else:
        print("add item to the cart")


# Write a program to login system with 3 attempts
"""
correct_password = "7891"
attempts = 1
while attempts <= 3:
    password = input("enter password: ")
    if password == correct_password:
        print("Login successful")
        break
    else:
        print("Wrong password")
        attempts += 1

if attempts == 4:
    print("Account is locked")

"""

# print odd numbers in the range of 0 to 9 using continue
# for i in range(0,9):
#     if i % 2 == 0: # even
#         continue
#     print(i) # we are skipping this operation for even values

# skip absent students during attendance
# students who are absent are skipped, but the loop
# number_of_students = int(input("enter number of students: "))
# for i in range(1, number_of_students):
#     status = input("Is Student {0} is present? ".format(i))
#     if status == "No":
#         continue
#     print("Student {0} is present, and attendance is marked".format(i))

a = 20
b = 30
print(a)
print(b)
del a
# print(a)

name = "kasi"
print(name)
# del name[0]  # immutable objject cannot be modified
del name
# 1. take the iformation from the use
# 2. sanitise the data
# 3. validate if custome is eligible
# 4. insert the data into the database
# 5. issue the voter card
# 6. reject with error message saying, customer is not eligible

'''
user_input_cricketer = input("Who is the odi top cricketer/batsman? ")
top_odi_batsman = "virat kohli"
if user_input_cricketer == top_odi_batsman: # True or False
    print("your answer is correct") # inside condition
    print("top odi batasman is virat")
else:
    print("your answer is incorrect")
print("End of the program") # outside if condition
'''

# ATM withdrawl
# user_pin_number = input("Please enter your pin number: ")
'''
withdraw_amount = float(input("Please enter your withdraw amount: "))

current_balance = 1200.50 # this has to come from database
# actual_pin = 7777 # this has to come from database

if withdraw_amount <= current_balance:
    print("Cash is successfully withdrawn")
else:
    print("!!!You have insufficient funds in your account")
   
'''

# voter criteria
'''age = int(input("Please enter your age: "))
state = input("Please enter your state: ")
current_state = "Telangana"
if age >= 18 and state == current_state:
    print("you are eligible for vote")
else:
    print("you are not eligible for vote")
'''

# if-elif-else
# Students Grades based on marks
# Here we have more than two possibilities(A, B, C, and Fail)
# Here we have to have only grade per marks
'''marks = int(input("Please enter your marks: "))
if marks >= 90:
    print("Grade A")
elif marks >= 75:
    print("Grade B")
elif marks >= 35:
    print("Grade C")
else:
    print("Fail")
'''

#Write a program to take emp annual salary and tell him the slab
# salary = float(input("Please enter your salary: "))
# if salary <= 400000:
#     print("Nil")
# elif salary <= 800000:
#     print("5%")
# elif salary <= 1200000:
#     print("10%")
# elif salary <= 1600000:
#     print("15%")
# elif salary <= 2000000:
#     print("20%")
# elif salary <= 2400000:
#     print("25%")
# else:
#     print("30%")


# nested if-else
# ATM withdrawl
'''
current_balance = 1200.50 # this has to come from database
actual_pin = 7777 # this has to come from database
user_pin_number = int(input("Please enter your pin number: "))
if user_pin_number == actual_pin:# outer if
    withdraw_amount = float(input("Please enter your withdraw amount: "))
    if withdraw_amount <= current_balance: # inner if
        print("Cash is successfully withdrawn")
    else:  # inner else
        print("!!!You have insufficient funds in your account")
else: # outer else
    print("you have entered incorrect number")
'''


# bank loan eligibility : 1crore
salary = float(input("Please enter your salary: "))
credit_score = float(input("Please enter your credit score: "))
if salary >= 100000.00:
    if credit_score >= 750:
        print("you are eligbible for loan, your loan is approved")
    else:
        print("you are not eligbible for loan, due to low credit score")
else:
    print("Based on your salary, you are not elgible for 1 crore loan")


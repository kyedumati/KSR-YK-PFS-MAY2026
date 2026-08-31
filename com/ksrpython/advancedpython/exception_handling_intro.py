a = 20
# if a = 20 # syntax error
#     print("value is matched")

# price = 1000
# gst = price * 0.08 # logical error: should be 0.18 -> no exception no syntax error, silently giving wrong total
# print(gst)
# balance =0
# def deposit(amount):
#     global balance
#     balance += amount
#     return balance
#
# amount = int(input("Enter amount:"))
# print(deposit(amount))

# final_amount = int(input("Enter amount to devide:"))
# no_of_friends = int(input("Enter number of friends:"))
# splitted_amount = final_amount/no_of_friends
# print("Splitted amount:", splitted_amount)


# we are handling exception with try and except blocks --> risky attempt, and exception recovery
def split_bill():
    try:
        final_amount = int(input("Enter amount to devide:"))
        no_of_friends = int(input("Enter number of friends:"))
        splitted_amount = final_amount/no_of_friends
        print("Splitted amount:", splitted_amount)
        return splitted_amount
    except ZeroDivisionError as e: # e= ZeroDivisionError("Devide by zero")
        print("You cannot divide by zero, please enter non-zero value no of friends", e.args[0])
    except ValueError as d:
        print("Enter a valid integer value")
    except Exception as e:
        print("You have encountered an error, please enter non-zero value no of friends or try again", e.args[0])
    finally:
        print("inside finally")



# try:
#     Step1: gather signup information from user
#     Step2: connect to database
#     print("aljdfajdfladfdj")
#     Step3: write data to database
# except Exception as e:
#     print("You have encountered an error to connecting to database")
# else:
#     Step3: write data to database
# finally:
#    Step4: close the database connection


# try:
#     pin = int(input("Enter pin number:"))
#     # if pin == 2222:
#     print("entered correct pin number")
# except ValueError as e:
#     print("Enter a valid integer PIN number")
# else:
#     print("Welcome to Landing Page")

try:
    amount = int(input("Enter amount:"))
    no_of_friends = int(input("Enter number of friends:"))
    share = amount/no_of_friends
# except ValueError:
#     print("need a numberic value")
except ZeroDivisionError, ValueError:
    print("You cannot divide by zero, please enter non-zero value no of friends")
else:
    print("Each person should pay", share)
finally:
    print("Split attempt finished")

# Program1: SecureBank PIN: except, else, finally ;, wrong pin validation, if pin is correct allow him to withdraw the amount, we have to exit from atm machine
# Program2: Order management: take an order from restaurant(biryani), calculate the bill, if biryani is over we have raise error, and once order is completed we have close the session

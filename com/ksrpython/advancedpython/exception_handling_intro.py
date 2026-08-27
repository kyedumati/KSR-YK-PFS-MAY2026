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
try:
    final_amount = int(input("Enter amount to devide:"))
    no_of_friends = int(input("Enter number of friends:"))
    splitted_amount = final_amount/no_of_friends
    print("Splitted amount:", splitted_amount)
except ZeroDivisionError as e: # e= ZeroDivisionError("Devide by zero")
    print("You cannot divide by zero, please enter non-zero value no of friends", e.args[0])
except ValueError as d:
    print("Enter a valid integer value")
except Exception as e:
    print("You have encountered an error, please enter non-zero value no of friends or try again")



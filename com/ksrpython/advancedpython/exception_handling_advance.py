class InsufficientFundsError(Exception):
    """ Insufficient funds """
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    pass

class InvalidAmountError(Exception):
    """ Invalid amount """
    pass


def withdraw(current_balance, amount): # anjali
    if amount <= 0:
        # print("You cannot withdraw less than zero") # suppressing the exceptions or error
        raise InvalidAmountError("You cannot withdraw less than zero") # shreyas
        # raise ValueError

    if amount > current_balance:
        # print("Insufficient funds") # suppressing/swallowing the exceptions
        raise InsufficientFundsError("Insufficient funds") #rithwik
    print("Withdraw is successful and current balance is:", current_balance)
    return current_balance - amount

'''
current_balance = 1000
try:
    amount = int(input("Enter amount:"))
    current_balance = withdraw(current_balance, amount)
# except ValueError as e:
#     print("Withrdraw failed: ", e.args[0])
# except InvalidAmountError as e:
#     print("Invalid amount: ", e.args[0])
except Exception as e:
    print(e)
# else:
#     print("Withdraw is successful and current balance is:", current_balance)
finally:
    print("you can collect the card, and exit from machine, thank you")
'''

class InvalidAgeError(Exception):
    """ Invalid age """
    pass

class UnderAgeError(Exception):
    """ Under age """
    def __init__(self, age, name, message= "You are under age"):
        self.age = age
        super().__init__(f"{age} : {name} you are under age")


def register_voter(voter_name, age):
    if age <=0:
        raise InvalidAgeError("You cannot register a voter with less than zero")

    if age <= 18:
        raise UnderAgeError(age, voter_name)

    print("You have registered a voter with ", voter_name)
    return voter_name

# try:
#     name = input("Enter your name: ")
#     age = int(input("Enter your age: "))
#     register_voter(name, age)
# except (InvalidAgeError,UnderAgeError) as e:
#     print(e)
# except Exception as e:
#     print(e)

# Write a program for InvalidRollNumberError with a rolle stored for a students
# search students with their roll number

class InvalidRollError(Exception):
     def __init__(self, roll, name, message= "Roll number is invalid"):
         self.roll = roll
         self.name = name
         super().__init__(f"{roll} : {name} you are entering invalid roll")


student_data = {
    101: {"name":"Rithwik", "mobileno": 632010, "address": "hyd"},
    102: {"name":"Anjali", "mobileno": 632011, "address": "narasaraopet"},
    103: {"name": "Shreyas", "mobileno": 632012, "address": "Kurnool"},
}

def find_student_by_rollno(rollno, name, student_data):
    if rollno not in student_data:
        raise InvalidRollError(rollno, name)
    return student_data[rollno]

try:
    rollno = int(input("Enter roll number: "))
    name = input("Enter name: ")
    student_info = find_student_by_rollno(rollno, name, student_data)
except InvalidRollError as e:
    print(e)
except Exception as e:
    print(e)
else:
    print(student_info)


# FileNotFoundError
# test_dict= {"name": "kasi"}
# print(test_dict["rollno"])









# I want to take two values from user and perform sum operation
# a = 40 # static input or hardcoded input
# b = 30 # static input or hardcoded input
# a = int(input("Enter a number: "))
# b = int(input("Enter another number: "))
# print(type(a))
# print(type(b))
# print(a+b)

# wreite a program to read employee data from keyboard and print that data
# empno= int(input("Enter a employee number: "))
# ename= input("Enter a employee name: ")
# eaddr= input("Enter a employee address: ")
# married= input("Enter a married status: ")
# salary= float(input("Enter a salary: "))
# print("Employee Name: ", ename)
# print("Employee Address: ", eaddr)
# print("Married Status: ", married)
# print("Salary: ", salary)

# reading multiple values at a time
# split() is the function in string, which will split values based on delimeter/saperator, if we dont specify any saperator
# by default it will saperate based on space(" ") and it will return splitted values in list type
# a = input("Enter 2 numbers in a space saperated:").split()
# print(type(a))
# print(a)
# print(int(a[0]) + int(a[1]))
# split_string = "kasi is a full stack trainer at KSR".split("kasi")
# print(split_string)
# a = input("Enter 3 float numbers in a comma saperated:").split(",")
# print(type(a))
# print(a)
# print(float(a[0]) + float(a[1]))

# eval()

# math_expression = input("Enter a math expression:")
# print(type(math_expression))
# print(math_expression)
# print(eval(math_expression))

# l = eval(input("Enter list of values"))
# print(list(l))
# print(type(l))


a = input("Enter a number:")
b = input("Enter another number:")
if a.isdigit() and b.isdigit():
    print(int(a)+int(b))
else:
    print("please enter value numberical values")
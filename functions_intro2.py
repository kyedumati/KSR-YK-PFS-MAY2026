# a=10 # global variable
#
# def f1():
#     print(a)
#
# def f2():
#     print(a)

# def f1():
#     a=10  # local variable
#     print(a)
#
# def f2():
#     print(a)
#
# a=10 # global variable
# def f1():
#     a = 777 # local variable
#     print(a)
#
# def f2():
#     print(a)
#
# f1()
# f2()
# print(a)
# print(a)


#
# a=10 # global variable
# def f1():
#     global a  # we are making a as global
#     a = 777 # we are updating global variable
#     print(a)
#
# def f2():
#     print(a)
#
# f1()
# f2()
# print(a)


# a=10 # global variable
# def f1():
#     a = 777 # local variable
#     print(a)
#     print(globals()['a'])
#
# def f2():
#     print(a)
#
# f1()
# f2()
# print(a)
# print(globals())

# write a program to find factorial of any given number : n value

# n = int(input("Enter a number to find factorial:"))
'''
#without recursion
def factorial(n):
    fact = 1
    for i in range(1,n+1):
        fact *= i
    return fact
'''
# with recursion
# def factorial(n): # n=5# n=4
#     if n == 0 or n == 1: # base case
#         return 1  # i'm caling factorial function again
#     return n*factorial(n-1) # recursive call/case # fact = 5*factorial(4) # fact = 5*4*factorial(3)  # fact = 5*4*3*factorial(2) # 5*4*3*2*1*factorial(0) # 5*4*3*2*1
#
#
# fact_output= factorial(n)
# print(fact_output)


# fibanocci series
# def fibanocci(n):
#     first = 0
#     second = 1
#     fibanocci_series = [first]
#     for i in range(2, n+1):
#         fibanocci_series.extend([second])
#         next_value = first + second
#         first = second
#         second = next_value
#
#     return fibanocci_series
#
# fibanocci_series = fibanocci(15)
# print(fibanocci_series)
fibanocci_series = []
def fibanocci(n):
    if n<=1:  # base case
        return n
    return fibanocci(n-1) + fibanocci(n-2) # recursive case

for n in range(10):
    print(fibanocci(n))

# HomeWork:
# Write a program to sum of N natural numbers with recursion
# Power of a number with recursion
# Reversing a string with recursion


#lambda expression
# write a program to create a lambda expression to find square of the given number
# def square(n):
#     return n*n
#
# print(square(5))

# square = lambda n: n*n
# print(square(5))
#
# # to find sum of 2 numbers
# s = lambda a,b: a+b
# print(s(3,4))
#
# # to find biggest of given values
# s = lambda a,b : a if a>b else b
# print(s(3,4))

# without lambda functions
# write a program to filter only even numbers from the list by using filter function?
# def isEven(n):
#     if n%2==0:
#         return True
#     else:
#         return False

l = [10,20,30,15,20,34,33,31]
# even_list = filter(isEven, l) # filter list by isEven function
even_list = filter(lambda n:n%2==0, l)
for i in even_list:
    print(i, end=" ")


# map() : WAP to double or square each item from the list
# without lambda
l = [1,2,3,4,5]

# def square_number(n): # functionality
#     return n**2


# squares_list = map(square_number, l)
squares_list = map(lambda x:x**2, l)
print(list(squares_list))


# write a funciton to sum all the items in the list
from functools import reduce
price_list = [120.12, 299.00, 499.00, 1299]

final_bill = reduce(lambda x,y:x+y, price_list) # Step1: 120.12+299.00 = [420.12, 499.00, 1299] # step2: 420.12+499.00 : [919.12, 1299] # step3: 2218.12
print(final_bill)


# function aliasing
def wish(name):
    print("Good morning", name)
    print("Good afternoon", name)

greeting = wish
print(id(wish))
print(id(greeting))

greeting("kasi")
wish("nani")


def outer():
    print("outer functions started")
    def inner():
        print("inside inner functions")
    print("outer function statement2")
    inner() # calling inner function

outer()
# inner() # NameError: name 'inner' is not defined. Did you mean: 'iter'?

def outer2():
    print("outer functions started")
    def inner2():
        print("inside inner functions")
    print("outer function statement2")
    return inner2

returned_iner = outer2()
print(returned_iner)
returned_iner()








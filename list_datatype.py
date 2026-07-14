# ways to create list
# empty list
cart = []
print(len(cart))
print(type(cart))

# add items to the cart
cart = ["pizza", "burger", "cake"]
print(len(cart))
print(type(cart))
print(cart[0])
print(cart[1])
print(cart[-1])

# students list with input function
# students = input("Please enter list of students: ")
# print(students)
# print(type(students))
# students = eval(students)
# print(students)
# print(type(students))

# using list()
l = list((10,20,30)) # to convert any other datatype to list
print(type(l))
print(l)

# using split()
statment= "python is very easy"
l = statment.split()
print(type(l))
print(l)


# accessing elements of the list using index and slicing
numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13]

print(numbers[0:5])
print(numbers[0:10:2])
print(numbers[::2])
print(numbers[1:10:2]) # 1 3 5 7 9 11
print(numbers[1::2]) # 1 3 5 7 9 11

for number in numbers:
    print(number)

i = 0
while i<len(numbers): # 0<13 True
    print(numbers[i]) # numbers[0] numbers[1] numbers[2].......
    i += 1

i = 0
while i<len(numbers): # 0<13 True
    print(numbers[i]) # numbers[0] numbers[1] numbers[2].......
    i += 2


# write a program to print only even numbers from list
# l = [2,1,4,6,10,12,14,15,19]
# for number in l:
#     if number % 2 == 0:
#         print(number)
#
# i = 0
# while i<len(l):
#     if l[i] % 2 == 0:
#         print(l[i])
#     i += 1

# 50 apples
# 50/5 = 10 times i ate apples
# 10/5 = 2apples is correct answer
apples = int(input("Enter how many apples:")) # this is the apples you initially got
while apples>=5:
    apples -= 5  # apples that you are eating
    apples += 1  # apples that you are getting in return after eating

print("apples remaining:", apples) # printing the remaining apples

# if i%5==0:
#     i+=1
# elif i%5!=0:
#     print(i)





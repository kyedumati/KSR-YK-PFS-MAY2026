emp_salaries = [1000, 2000, 3000, 2400,3000, 4000, 50000, 60000]
print("Before bonus:", emp_salaries)
# emp_salaries[0] += 100000
# emp_salaries[1] += 100000
# emp_salaries[2] += 100000
# emp_salaries[3] += 100000
for salary in emp_salaries: # salary is a variable which holds single value in every iteration
    salary += 100000
    print(salary)
# print("After bonus: ", emp_salaries)

# wap to print each character in the string
# name = input("Enter your name: ") # kasi
# for ch in name:
#     print(ch)

# wap to print chars present in string with index number
# index = 0
# for ch in name:
#     print("Character present at index:", index, "value is", ch)
#     index += 1

# Display sequence numbers from 1 to 20
for x in range(1, 21):
    print(x)

# Wap to print only even numbers from 20 to 40
# Step1: I need generate sequence number from 20 to 40 --> range(20,41)
# Step2.1: iterate each value in range : for i in range(20,41)
# Step2.2: check if given number is even --> number%2==0
# Step3: print the number that is satisfied in step2: if number%2==0
# print("Even numbers program")
# for number in range(20,41):
#     if number % 2 == 0:
#         print(number)

# wap to print odd numbers between 30 to 50
# print("Odd numbers program")
# for number in range(30,50):
#     if number%2!=0:
#         print(number)


# I want to ask all my students their marks and then calcular the average
# Step1: first ask the teacher to enter how many students :
# Step2: ask to enter marks of each student
# Step3: total+=marks
# Step4: calculate average = total/n
'''
numbers_of_students = int(input("Enter number of students?"))
total = 0
for i in range(numbers_of_students):
    marks = int(input("Enter marks of each student {0}".format(i+1)))
    total += marks

print("Total", total)
average = total / numbers_of_students
print("Average:",average)
'''

# Dmart store billing
# check how many items are purchased
# ask the price of each item
# calculate final Bill
number_of_items = int(input("Enter number of items?"))
total_bill = 0.0
for i in range(number_of_items):
    price = float(input("Enter price of item {0}".format(i+1)))
    total_bill += price

print("----------------------")
print("Total bill:", total_bill)







# To print numbers from 1 to 10 by using while
x = 1
while x<=10: # True
    print(x)
    x+=1

print("exit while loop")

# Write a program to print sum of first N numbers
# 1+2+3+4+5 = 15
# sum = 0
# for i in range(1,6):
#     sum += i
# print(sum)
# N = int(input("Enter number of items you want to sum:"))
# i = 1
# sum = 0
#
# while i<=N: # starts with i=1 and ends with N
#     sum += i
#     i+=1
# print(sum)


# WAP to print Mobile PIN verification
# until user enters the correct PIN, we have to give a try again message
# i want to close the program when user execeeds 3 attempts
correct_pin = 7777
user_entered_pin = int(input("enter pin number: "))
exceeding_number = 1
while correct_pin!=user_entered_pin and exceeding_number<3:
      print("you've entered incorrect pin number")
      user_entered_pin = int(input("enter pin number again: "))
      exceeding_number+= 1

if exceeding_number>=3 and correct_pin!=user_entered_pin:
    print("you've exeeced the maximum number of attempts")
elif correct_pin==user_entered_pin:
    print("Login successful")

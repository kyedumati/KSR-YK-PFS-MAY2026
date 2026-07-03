# write a program to print 1to4 numbers in rectangle
for i in range(1,5): # outer for loop
    for j in range(1,5): # inner for loop
        print(j, end=" ")
    print() # outer for loop

# Write a program to display * in the right angle trangle form
# *
# * *
# * * *
# * * * *
# * * * * *
for i in range(1,10):
    for j in range(1, i+1): # 1, 1+1 :  1,2+1 : 1, 3+1: 1,4+1 :  1,5+1
        print("*", end=" ")
    print()


for i in range(1,10):
    for j in range(1, i+1): # 1, 1+1 :  1,2+1 : 1, 3+1: 1,4+1 :  1,5+1
        print(j, end=" ")
    print()

#1. Write a program to count even and odd numbers from list
# Input: ex: [10,21, 4, 45, 66, 93,11, 13, 15]
# Output: Even numbers: 3 # even_count
# Odd numbers: 6

# num % 2 == 0 this confirms even
# if it is even number count has to increase  : even_count+=1
# finally print even_count
numbers = [10,21, 4, 45, 66, 93,11, 13, 15, 16, 19]
even_counter = 0
odd_counter = 0
for item in numbers:
    if item % 2 == 0:
        even_counter += 1
    else:
        odd_counter += 1
print("Even numbers:", even_counter)
print("Odd numbers:", odd_counter)

# 2. Reverse a list
# Ex: Input: [100,200,300, 400]
# output: [400,300,200,100]
l = [100,200,300, 400]
print(l[::-1])

# 3. swap two element at given indices
#Input: [23, 65, 19,90]
# 0 and 2
# ouput: [19, 65, 23, 90]
list_data = [23, 65, 19,90]
idx1, idx2 = 0, 2
list_data[idx1], list_data[idx2] = list_data[idx2], list_data[idx1]
print(list_data)

# 4. Find the longest string in the a list
# Ex: input: ["PHP", "Java","Python", ".Net", "C#"]
# output: Python
languages = ["PHP", "Java","Python", ".Net", "C#"]
max_length_word = ""
max_length = 0
for language in languages:
    lang_length = len(language) # 3 , 4, 6, 4, 2
    if lang_length > max_length: # 3>0= 3,  4>3=4, 6>4=6, 4>6, 2>6
        max_length_word = language # "PHP", "Java", "Python"
        max_length = lang_length # 3, 4 , 6

print("max length word:", max_length_word)
print(max_length)

longest_word = max(languages, key=len)
print(longest_word)

#5. to square every item in the list
#ex:Input: [2,3,4,5,6]
#Ouput: [4,9,16,25,36]
numbers = [2,3,4,5,6]
squred_numbers = []
for i in numbers:
    squred_numbers.append(i**2)
print(squred_numbers)

#list comprehension
squred_numbers = [i**2 for i in numbers] # i is squared for every item in the numbers -> that will stored in the list []
print(squred_numbers)

# 6. count occurances of each item in the list
# input: [10,10,20,30,10,34,40,40,20,30]
# ouput : 10 --> 3
# 20 --> 2
# 30 --> 2
# 34 --> 1
# 40 --> 2
numbers = [10,10,20,30,10,34,40,40,20,30]
# n = int(input("Enter a number to find out the count:"))
# counters = 0
# for i in numbers:
#     if n == i:
#         counters += 1
# print(n,"is appeared: ", counters, "times")
# print(n,"is appeared: ", numbers.count(n), "times")


# 7. Remove all occurances of a specifc item
numbers = [10,10,20,30,10,34,40,40,20,30]
# ouput: [20,30,34,40,40,20,30]
x = 10
# approach1:
cleaned_list = [i for i in numbers if x!=i]
print(cleaned_list)
# approach2:
for item in numbers:
    if x in numbers:
        numbers.remove(x)
print(numbers)

# 8. Filter numbers from the list : only prime numbers
# input: list = [4,7,9,11,13,16,19]
# ouput: [7,11,13,19] # prime
numbers = [4,7,9,11,13,16,19] # I need to find out prime number
# for i in numbers: # to iterate each item from original list
# n = 9
prime_list = []
for n in numbers:
    counter = 0
    for i in range(2, n): # prime number
        if n % i == 0:
            counter += 1
            break
    if counter == 0:
        prime_list.append(n)
    else:
        print(n, "is not the prime number")

print("prime_list: ", prime_list)

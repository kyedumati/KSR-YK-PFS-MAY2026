# important programs : string concept
# 1. Write a program to reverse a string
# Input: virat kohli
# Output: ilhok tariv

# 1st approach
# s = input("Enter a string:")
# print(s[::-1])

#2nd approach: without using slice operator
# take the input from the user
# first find out last index number : using len()-1
# we have to read the every character from last index to first index 0
# which means we have to iterate a loop until 0 starts from last index
'''
s = input("Enter a string:")
last_index = len(s) - 1
output_string = ''
while last_index >= 0:
    # print(s[last_index], end='')
    output_string += s[last_index]
    last_index -= 1
print(output_string)
'''

# Write a program to reverse order of words
# Input: Learning Python Is Very Easy
# Outuput: Easy Very Is Python Learning

# First step : split the string with words: s.split() : it will return list of words
# Second Step: you got the list of words ['Learning', "Python","Is", "Very", "Easy"]
# Third step : using list indexing we have to reverse the items
# first find out last index number : using len()-1
# we have to read the every character from last index to first index 0
# which means we have to iterate a loop until 0 starts from last index

'''
s = input("Enter a string:")
splitted_string_list = s.split() # list of string words
print("splitted_string_list: ", splitted_string_list)
last_index = len(splitted_string_list) - 1
new_list = []

while last_index >= 0:
    new_list.append(splitted_string_list[last_index])
    last_index -=1
print("new list", new_list)
print(' '.join(new_list))
'''

# Write a program to reverse internal content of each word
# input: Virat Kohli
# output: tariV ilhoK

# input2: MS dhoni
# output2:SM inohd

# Step1: split the string, so that each word will be saperated to the list
# Step2: list = ["MS", "Dhoni"]
# Step3: pick each item from the list : list[0], list[1]
# Step4: picked item(word) reverse it
# step5: initialise one empty list to take the output and add the reversed word at step4 to new list
# Step6: join the string which are in the list
'''
s = input("Enter a string:")
splitted_string_list = s.split()
print("splitted_string_list: ", splitted_string_list)
output_list = []
for word in splitted_string_list: #step3
    reversed_word = word[::-1] #step4
    output_list.append(reversed_word) #step5

print("output_list: ", ' '.join(output_list))
'''






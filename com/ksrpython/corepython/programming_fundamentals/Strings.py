cricketer = "Virat Kohli"
print(cricketer)

print(cricketer[0])
print(cricketer[2])
print(cricketer[-3])
# print(cricketer[40])  # I want to get 40th index value

# how to get multiple characters using indexing/slicing
print(cricketer[6:11])
print(cricketer[6:])
print(cricketer[6:40])

print("invalid start and end:"+ cricketer[16:40])

print(cricketer[:]) # : by default starting position 0 and ending position will take it length of the string
print(cricketer[:11])
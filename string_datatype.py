name = "virat kohli"
print(name[0:5])
print(name[0:5:1])
print(name[0:11:2])# 0 2 4 6 8 10 --> vrtkhi

print(name[:7]) # name[0:7:1]
print(name[::2]) # name[0:11:2]
print(name[::-2]) # name[-1:-12:-2]
print(name[::-1])
print(name[:-2]) # name[0:-2]

# len()
print(len("virat kohli"))
print(len(name))
print(name[0:len(name)-2]) # name[0:9]
'''
given_string = input("Enter a string: ")
substring = input("Enter a substring: ")
print(given_string)
print(substring)

if substring in given_string:
    print(substring, "is found in main string")
else:
    print(substring, "is not found in main string")
'''
# print("     virat kohli".lstrip())
# print("     virat kohli     ".rstrip())
# print("     virat kohli     ".strip())
# state = input("Enter a state: ")
# if state.strip() == "Telangana":
#     print(state, "is in Telangana", "eligible for vote")
# else:
#     print(state, "is not in Telangana", "not eligible for vote")


s = "Learning python is very easy, python is open source programming language"
print(s.find("python"))
print(s.find("Learning"))
print(s.rfind("python"))
print(s.find("kasi"))

name = "virat kohli"
print(name.find("a", 1, 10))

print(s.index("python"))
print(s.index("python"))
print(s.index("Learning"))
print(s.rindex("python"))
# print(s.index("kasi")) # ValueError: substring not found

print(s.count("Python"))
print(s.count("python"))
print(s.count("python", 6,15))
s2= "aabbccabcde" #

print(s.replace("easy", "difficult"))

print(s.replace("difficult", "easy"))
print(s2.replace("a", "z"))
print(s2)
s3 = s2.replace("a", "z") # you are creating new object to hold the replaced value, because of immutability

print(s.split("python"))
print(s.split(","))
print(s.split()) # by default space will be the saperator

students = ["kasi", "virat", "dhoni"]
s = '-'.join(students)
print(s)
print('&'.join(students))
print('1111'.join(students))


s = "learning Python is very easy"
print(s.upper())
print(s.lower())
print(s.swapcase())

print("kasi yedumati".title())
print("KaSI yedUMati".title())
print(s.title())
print(s.capitalize())
print("kasi yedumati".capitalize())

print(s.endswith("easy")) # is string s is ending with easy ? YES True
print(s.startswith("easy"))
print(s.startswith("learning"))

students = ["kasi", "virat", "dhoni", "divya", "anjali", "bhuvan", "harika", "chandu", "shreyas"]
for student in students:
    if student.endswith("a"):
        print(student)
    else:
        continue

# checking the type of characters in present in a string
print("=======checking the type of characters in present in a string==============")
print("kasi1234".isalnum())
print("kasi".isalnum())
print("abcd1234".isalpha())
print("abcd".isalpha())
print("1234".isdigit())
print("xyz123".isdigit())
print("abcd".islower())
print("abcD".islower())
print("XYZ".isupper())
print("zYz".isupper())
print("kasi".istitle())
print("Kasi".istitle())
print("      ".isspace())
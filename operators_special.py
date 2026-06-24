a = 20
b = 30
c = 30
print(a is b) # a and b has same address of the object
print(a is not b)
print(a is c)
print(b is c)
print(id(a))
print(id(b))
print(id(c))
x = True
y = False
z = True
print(x is y)
print(x is z)
print(x == y)
print(b == c)
print(b is c)


list1 = ["kasi", "yedumati", "python"]
list2 = ["kasi", "yedumati", "python"]
print(id(list1))
print(id(list2))
print(list1 is list2) # address comparision
print(list1 == list2) # content comparision
# list1.append("java")

print(id(list1))
print(id(list2))


# membership operators
students_attendance = ["Bhavan", "Chandu", "Anjali", "Varshith", "divya", "Harika", "Pooja", "Shreya"]
print("mahesh" in students_attendance)
print("mahesh" not in students_attendance)

if "mahesh" in students_attendance:
    print("mahesh is available in the class")
else:
    print("mahesh is not available in the class")

hello_python = "Hello Everyone, Python is very easy"
print("easy" in hello_python)
student_name = "mahesh babu"
print("i" in student_name)

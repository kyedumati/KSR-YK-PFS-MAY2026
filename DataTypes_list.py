student_names = ["kasi", "bhuvan", "chandu", "varshith", "harika", "chandu"]
marks = [98, 60, 40, 50, 60, 80] # duplicate data is allowed
print(student_names)
print(marks)

print(type(student_names))
print(student_names[3])
print(student_names[-2])
# student_name_at_3 = student_names[3] # varishith
# print(student_name_at_3)
# print(type(student_name_at_3))
# print(student_name_at_3[2])
print(student_names[3][2])
print(student_names[-2][3])
# i ant to print U from bhuvan using negative index
print(student_names[-5][-4])

# print(marks[2][1])
chandu_marks = marks[2] # 40 integer values
chandu_marks = str(chandu_marks)[1]

print(chandu_marks)
print(type(chandu_marks))

marks[2] = 95 # modification is possible
print(marks)

student_names.append("divya")
student_names.append("shreyas")
student_names.append("Anjali")
print(student_names)
student_names.remove("kasi")
print(student_names)






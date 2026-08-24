class Student:
    def __init__(self, name, age, rollno):
        self.name = name
        self.age = age
        self.rollno = rollno

    def submit_homework(self):
        print("Homework Submitted")

    # def display(self):
    #     return f"{self.name}, {self.age}, {self.rollno}"
    def __str__(self):
        return f"{self.name}, {self.age}, {self.rollno}"


student = Student("kasi", 21, "1122")
# print(student.display())
print(student)

# Readable BankAccount, Product information


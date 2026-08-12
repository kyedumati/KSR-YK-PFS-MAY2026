# write a class for employee portal for ksr datavizion company : empiid, salary, name, email
class Employee:

    company_name = "KSR Datavizon" # static or class variable

    def __init__(self, empid, name, salary):
        self.email = None
        self.empid = empid # instance variable
        self.name = name
        self.salary = salary

    def display_employee(self, email): # instance method
        title = "Staff" # local variable
        print(title)
        print(self.empid)
        print(self.name)
        print(self.salary)
        print(self.email)
        print(Employee.company_name)
        self.email = email # intialise instance variable at instance method

emp1 = Employee(1, "Kasi", 123000)
print(emp1.salary)
print(emp1.empid)
print(emp1.email)
emp1.email = "kasi@gmail.com" # instance variable initialisation
print(emp1.email)
print(emp1.company_name)


emp2 = Employee(2, "Naveen", 120000)
print(emp2.salary)
print(emp2.company_name)
print(Employee.company_name)
# print(Employee.email) #













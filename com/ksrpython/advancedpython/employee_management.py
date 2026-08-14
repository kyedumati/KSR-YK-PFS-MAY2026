# you are a person today : atributes: name, mobile: features: learning, chitchatting, roaming,

# you will be an employee tomorrow once you get an offer : attributes: name, mobile, empid, balance: features: learning, earning, chitchatting, roaming, movies
# , chuttala yedupu

class Person:
    def __init__(self, name, mobile):
        self.name = name
        self.mobile = mobile

    def greet(self):
        return "hi, my name is " + self.name

    def learning(self):
        print("learning as a person")


class Employee(Person): # Employee IS-A person
    def __init__(self, name, mobile, balance, employee_id):
        super().__init__(name, mobile)
        self.balance = balance
        self.employee_id = employee_id

    def working(self): # employee specific feature
        print("working as a person")

emp1 = Employee("Priya", "98765432", 220000.34, 1234)
print(emp1.greet())
emp1.learning()
emp1.working()





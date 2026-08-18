# laptop is owned by person and person is a employee


class Laptop:
    def __init__(self, name, model, price):
        self.name = name
        self.model = model
        self.price = price

    def specification(self):
        return "name: " + self.name + "\n" + "model: " + self.model + "\n" + "price: " + str(self.price)

class Person:
    def __init__(self, name, mobilenumber, address):
        self.name = name
        self.mobilenumber = mobilenumber
        self.address = address

    def greeting(self):
        return "hi... I am" + self.name

class Employee(Person): # IS-A relationship
     def __init__(self, name, mobilenumber, address, empid, laptop):
         super().__init__(name, mobilenumber, address)
         self.empid = empid
         self.laptop = laptop # HAS-A relationship  :  HAS-A Laptop

     def information(self):
         print(self.laptop.specification()) # he is calling or using laptop
         return self.greeting() + " " + str(self.mobilenumber) + " " + self.address + " " + str(self.empid)

laptop = Laptop("Lenovo", "Thinkpad 420", 120000)
manager = Employee("Priya", 9876543, "hyderabad", 1234, laptop)
print(manager.information())





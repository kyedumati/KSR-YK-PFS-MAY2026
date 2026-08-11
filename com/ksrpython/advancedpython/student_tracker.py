# using object oriented
# class Student:
#      def __init__(self, roll, name, marks):
#          self.roll = roll
#          self.name = name
#          self.marks = marks
#
#      def average(self):
#          marks = self.student["marks"]
#          return sum(marks) / len(marks)  # average formula
#
#      def grade(self):
#          avg = self.average(self)
#          if avg >= 90:
#              return "A"
#          elif avg >= 80:
#              return "B"
#          elif avg >= 70:
#              return "C"
#          elif avg >= 50:
#              return "D"
#          else:
#              return "Fail"
#
#      def is_pass(self):
#          if self.grade(self) == "Fail":
#              return False
#          else:
#              return True
#
#      def display(self):
#          print(self.roll, ": ", self.roll, " - ", self.grade())

# A class is blueprint
# an object is a one concrete instance of that class
# __init__ is a constructor which initialises data of that object, __init__ will be call whenever you create a new object and set data.

# s1 is a reference to that object in memory, we use it to call methods and attributes
# __init__ will be called automatically whenever an object is created --> we don't have call by its name

#


# self a keyword
class Student:
    # initialise properties
    def __init__(self, roll, name, marks, email): # this is a constructor to initialise properties of the object
        self.roll = roll
        self.name = name
        self.marks = marks
        self.email = email

    def average(self):
        return sum(self.marks) / len(self.marks)

    def grade(self):
         avg = self.average()
         if avg >= 90:
             return "A"
         elif avg >= 80:
             return "B"
         elif avg >= 70:
             return "C"
         elif avg >= 50:
             return "D"
         else:
             return "Fail"

    def is_pass(self):
        if self.grade() == "Fail":
            return False
        else:
            return True

    # @classmethod
    # def test(cls):
    #     print("test")

    def display(self):
        print(self.roll, ":" , self.name, ":", self.grade())

# s1 = {"roll": 100, "name": "", "grade": 80, "email": ""}
s1 = Student("123", "kasi", [98,78,67], "kasi@gmail.com") # creating an object
s1.display()
s1.display()
s1.display()
# s2 = Student("234", "naveen", [96,79,68], "naveen@gmail.com") # TypeError: Student.__init__() takes 4 positional arguments but 5 were given

s2 = Student("222", "naveen", [98,79,68], "naveen@gmail.com")
s2.display()
if s2.is_pass():
    print(s2.name, "Passed")
else:
    print(s2.name, "Failed")

print(s2.roll)
# l = list((1,2,3,4))
# s = set((1,2,3))


class Car:

    def __init__(self, model, year, engine_capacity): # initializing car object
        self.model = model
        self.year = year
        self.engine_capacity = engine_capacity

    def display(self): # displaying car info
        print(self.model, self.year, self.engine_capacity)

nexon_car = Car("nexon", "2020", 2)
nexon_car.display()

sierra_car = Car("sierra", "2026", 3)
sierra_car.display()



# Write a program to create a product for ecommerce site: using class and object:  properteies(sku, price, quantity, productname): behavior: display, product_purchase
# Write a porgram to create a BankAccount for bank site: properties(balance, name, address, email, mobilenumber): behaviour : deposit, withdraw and bank balance
#















# I have to build a plan for vehicles: car, bus, etc......
from abc import ABC, abstractmethod

class Vehicle(ABC): # abstract class
    def __init__(self, engine, brand, model):
        self.engine = engine
        self.brand = brand
        self.model = model

    @abstractmethod
    def no_of_wheels(self): # abstract method
        pass

    def specs(self):
        return self.engine, self.brand, self.model
#
# class Bus(Vehicle): # bus will also be treated abstract class, and we cant create object for this
#     def test(self):
#         print("Bus test")
#

class Bus(Vehicle): # child class
    def __init__(self, engine, brand, model):
        super().__init__(engine, brand, model)

    def no_of_wheels(self):
        return 8

class Bike(Vehicle):
    def no_of_wheels(self):
        return 2

bus_obj = Bus("testengine", "testbrand", "testmodel")
bike_obj = Bike("testengine", "testbrand", "testmodel")
print(bus_obj.no_of_wheels())
print(bike_obj.no_of_wheels())
print(bike_obj.specs())
print(bike_obj.no_of_wheels())


# Shared deposit, abstract kind()
class Account(ABC):
    def __init__(self, holder, balance=0):
        self.holder = holder
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount")
            return
        self._balance += amount

    def get_balance(self):
        return self._balance

    @abstractmethod
    def kind(self): # to return what type of account it is
        pass

class SavingsAccount(Account):
    def __init__(self, holder, balance=0):
        super().__init__(holder, balance)

    def kind(self):
        return "savings"

    def __str__(self):
        return self.holder + " balance:" + str(self._balance)

savings_obj = SavingsAccount("kasi yedumati", 100)
print(savings_obj)
print(savings_obj.kind())


# Medical care report generation: abstract report + shared header
class Report(ABC):
    def __init__(self, patient):
        self.patient = patient

    def header(self):
        return "MedCare: Apollo Hospital" + self.patient

    @abstractmethod
    def title(self):
        pass

class LabReport(Report):
    def __init__(self, patient):
        super().__init__(patient)

    def title(self):
        return "Blood Test"

class InvoiceReport(Report):
    def __init__(self, patient):
        super().__init__(patient)

    def title(self):
        return "Invoice Bill"

lab_report_obj = LabReport("kasi yedumati")
print(lab_report_obj)
print(lab_report_obj.title())
invoice_obj = InvoiceReport("kasi yedumati")
print(invoice_obj)
print(invoice_obj.title())
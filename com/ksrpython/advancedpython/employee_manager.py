# wap to maintain relation between employee and manager, and then print their net salary and payslip
class Employee:
    def __init__(self, name, basic_pay):
        self.name = name
        self.basic_pay = basic_pay

    def net(self):
        return self.basic_pay * 0.9

    def payslip(self):
        return "{0} basic pay is:{1} and net pay: {2}".format( self.name, self.basic_pay, self.net())

class Manager(Employee): # IS-A : Aggregation
    def __init__(self, name, basic_pay, bonus):
        super().__init__(name, basic_pay)
        self.bonus = bonus

    def net(self): # it is overridden method
        return self.basic_pay * 0.9 + self.bonus

    # def payslip(self):
    #     return self.name + "basic pay is:"+ self.basic_pay + " and net pay: " + self.net()


employee = Employee("Kasi", 12000.00)
print("Employee payslip", employee.payslip())
manager = Manager("Naveen", 30000.00, 5000)
print("Managers payslip", manager.payslip())
        
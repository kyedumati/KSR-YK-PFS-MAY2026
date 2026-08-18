class Person:
    def role(self):
        print("Role is person")

    def chit_chat(self):
        print("chit chatting")

class Employee(Person): #
    def working(self):
        print("working")

    def role(self): # overridden method
        print("role is employee")

class Manager(Employee):
    def giving_hikes(self):
        print("giving hiking")

    def role(self): # overridden method
        print("role is manager")


manager = Manager()
manager.role()
manager.chit_chat()
manager.working()

print("Is Manager is a Person?:", isinstance(manager, Person)) # manager --> went outside -->people are recognising him becuase, he has similar face cuts of person

for o in Manager.mro():
    print(o)

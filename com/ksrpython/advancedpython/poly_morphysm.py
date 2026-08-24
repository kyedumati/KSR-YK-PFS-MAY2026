#
'''def checkout(payment_type, amount):
    if payment_type == "upi":
        print("Paid via: UPI"+ "amount: "+str(amount))
    elif payment_type == "card":
        print("Paid via: CARD"+ "amount: "+str(amount))
    elif payment_type == "cash":
        print("Paid via: CASH"+ "amount: "+str(amount))
    else:
        print("Unknown payment type")

checkout("upi", 100)
checkout("card", 100)
checkout("cash", 100)


'''
class PaymentType:
    def pay(self, amount):
        pass

class UPI(PaymentType):
    def pay(self, amount):
        print("Paid via UPI pay: "+ str(amount))

class Card(PaymentType):
    def pay(self, amount):
        print("Paid via CARD pay: "+ str(amount))

class Cash(PaymentType):
    def pay(self, amount):
        print("Paid via Cash pay: "+ str(amount))


def checkout(payment_type, amount):
    payment_type.pay(amount)

checkout(UPI(), 100)  # customer is calling checkout function after selecting payemnt mode
checkout(Card(), 100)
checkout(Cash(), 100)
# checkout("kasi", 200)



# override polymorphism, same method name on parent/children
class Vehicle:
    def info(self):
        print("Vehicle info")

class Bike(Vehicle):
    def info(self):
        print("Bike info")

class Car(Vehicle):
    def info(self):
        print("Car info")


for v in [Car(), Bike(), Car()]:
    v.info()       # same call site, we are able call different object using same call




class Addition:
    # def add(self, a, b):
    #     return a+b
    #
    # def add(self, a, b, c):
    #     return a+b+c

    def add(self, *args):
        return sum(args)

print(Addition().add(1, 2)) # typeError: missing c
print(Addition().add(1, 3, 4))



# find a circle, square and any possible mathematical shapes using ooops






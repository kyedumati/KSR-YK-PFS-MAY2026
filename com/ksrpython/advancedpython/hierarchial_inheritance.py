class Vehicle:
      def __init__(self, brand, model, year):
          self.brand = brand
          self.model = model
          self.year = year

      def start(self):
          return self.brand + "starting...."

class Bike(Vehicle):
    def info(self):
        return "Bike: " + self.brand

class Car(Vehicle):
    def info(self):
        return "Car: " + self.brand


car_obj = Car("Tata", "Nexon", "2026")
print(car_obj.start())
print(car_obj.info())

bike_obj = Bike("Royal Enfield", "classic 350", "2022")
print(bike_obj.start())
print(bike_obj.info())


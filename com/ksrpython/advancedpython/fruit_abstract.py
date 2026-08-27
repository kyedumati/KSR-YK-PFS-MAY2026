from abc import abstractmethod, ABC

# normal class, abstract method
class Test: # concrete class
    # def test_info(self):
    #     pass
    pass

# class Fruit(ABC):
#     pass

# it is extending ABC and has one abstract method
# class Fruit(ABC):
#     @abstractmethod
#     def taste(self):
#         pass

# abstrac method, but does not extend ABC: without ABC, the decorator is only documentation, it doesn't block object to create
class Fruit:
    @abstractmethod
    def taste(self):
        print("taste")

# t = Test()
# # print(t.test_info()) # we are able
# print("Object is created")

fruit_obj = Fruit()
print(fruit_obj)
fruit_obj.taste()



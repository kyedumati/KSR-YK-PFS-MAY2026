from abc import abstractmethod, ABC


class Fruit(ABC):
    @abstractmethod
    def taste(self):
        pass # abstract

    def display_fruit(self):
        print("test fruit") # implemention method


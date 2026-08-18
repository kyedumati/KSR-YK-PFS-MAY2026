# here, if an inheritance contains one child, with multiple parents
class Father:
    def skills(self):
        return "Driving"

class Mother:
    def skills(self):
        return "Cooking"

class Child(Mother, Father): # multiple inheritance
      def all_skills(self):
          # MRO: child --> Father -> Mother -> object
          return Father.skills(self) + Mother.skills(self)


child_obj =  Child()
print(child_obj.all_skills())
print("MRO:", [x.__name__ for x in Child.mro()])
print("Which skills() wins alone?", child_obj.skills())




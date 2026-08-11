# To get information about about list
cart = ["pizza", "burger", "coke", "pizza", "coke", "beer"]
print(len(cart))
print("pizza count is:", cart.count("pizza"))
print(cart.index("burger"))
print(cart.index("pizza"))
# print(cart.index("biryani"))

if "biryani" in cart:
    print(cart.index("biryani"))

# manipulating the data
cart.append("biryani")
cart.append("sprite")
print(cart)
cart.insert(2, "biryani")
cart.insert(6, "pen")
print(cart)
cart.extend(["biryani", "pen"])
print(cart)
cart[0] = "chocolate" # to update or replace existing items
print(cart)
cart.remove("biryani")
print(cart)
# if "dark fantasy" in cart:
cart.remove("dark fantasy")

popped_value = cart.pop()
print(cart)
print("popped value is:", popped_value)
cart.pop()
print(cart)
print(cart.pop(2))
print(cart)
# cart.pop(10) IndexError: pop index out of range

# ordering of the list
cart = ["pizza", "burger", "coke", "pizza", "coke", "beer"]
print(cart)
cart.reverse()
print(cart)
cart.sort()
print(cart)
ranks = [1,12,32,56,3,4,5]
ranks.sort()
print(ranks)
student_info = ["kasi", 95, "1234"] # "kasi" < 95
# student_info.sort() #
print(student_info)
x = [10,20,100,2,5]
# x.sort(reverse=False) # ascending order
x.sort(reverse=True) # descedning order
print(x)




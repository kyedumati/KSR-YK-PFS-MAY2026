# To get information about about list
cart = ["pizza", "burger", "coke", "pizza", "coke", "beer"]
print(len(cart))
print("pizza count is:", cart.count("pizza"))
print(cart.index("burger"))
print(cart.index("pizza"))
# print(cart.index("biryani"))

if "biryani" in cart:
    print(cart.index("biryani"))

t = ()
print(type(t))
t = (10,)
print(type(t))
t = (10,20,30,40,50)
t = 10,20,30,40
print(type(t))

a = 20
b = 30
c = 40
t = a,b,c # this is called tuple packing
print(t)
print(type(t))
x,y,z = t # unpacking
print(x)
print(y)
print(z)
# x,y = t
# print(x)
# print(y)
t2 = ("kasi", 20, 23.5)
x,y,z = t2
print(x)
print(y)
print(z)

squares = [x**2 for x in range(10)] # list comprehension
print(squares)
print(type(squares))

squares = (x**2 for x in range(10)) # tuple comprehension
print(squares)
print(type(squares))
for i in squares:
    print(i)


# write a program to print student marks report using tuypel packing and unpacking
# and calculate total and average marks
student = ("Rahul", 1001, 89, 92, 95)
name, rollno, sub1, sub2, sub3 = student
total = sub1 + sub2 + sub3
average = total/3
print("Name: ", name)
print("Rollno: ", rollno)
print("Total: ", total)
print("Average: ", average)

# write a program to find price of any product that user is looking for
products = (("Laptop", 65000), ("mouse", 250), ("monitor", 15000), ("keyboard", 1500))
product_name = input("Enter product name: ")
is_product_found = False

for product in products:
    # print(product)
    if product[0].lower() == product_name.lower():
        print("Price:", product[1])
        is_product_found = True
        break

if not is_product_found:
    print("Product not found")





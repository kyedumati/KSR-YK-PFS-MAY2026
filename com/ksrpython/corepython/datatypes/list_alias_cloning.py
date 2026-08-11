# aliasing
# x = [10,20,30,40,50]
# print(id(x))
# y = x
# print(id(y))
#
# x[1] = 100
# print(x)
# print(y)

# aliasing
cart = ["laptop", "mouse", "keyboard"]
backup_cart = cart  #aliasing
print("oringal cart", cart)
print("backup cart", backup_cart)
cart.remove("laptop")
print(cart)
print(backup_cart)
print(id(cart), id(backup_cart))


# cloning using copy() function
students = ["rahul", "anil", "kiran"]
backup_students = students.copy() # it gets all the content of the students or original list
students.remove("rahul")
print(students)
print(backup_students)

# closing using slice operator
# students[0:3] # first item to 3rd item
marks = [60,70,80,90, 99]
backup_marks = marks[:] # this is to get all items from students list
marks.remove(60)
print(marks)
print(backup_marks)

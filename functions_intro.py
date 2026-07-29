# a = 10
# b = 20
# c = a+b
# print(a)

# len("kasi")
# a = "kasi"
# str_length = 0
# for i in a:
#     str_length += 1
# print(str_length)

def addition(a, b):
    c = a+b
    return c

print(addition(10,20)) # way to call a function
print(addition(30,40))
addition(100,200)
sum_value = addition(300,400)
print(sum_value)

# write a function to take name of the student as input and print wish message by name
def wish_student(name):
    print("Hello", name, "Good morning")

wish_student("Rithwik")
wish_student("Anjali")
print(wish_student("Divya"))

# write a function to check whether the given number is even or odd
def even_odd(number):
    if number % 2 == 0:
        print(number,"is even")
    else:
        print(number, "is Odd")

even_odd(10)
even_odd(20)
even_odd(5)
even_odd(9)




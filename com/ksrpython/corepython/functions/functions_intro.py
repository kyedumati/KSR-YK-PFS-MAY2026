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


# write a function to take name of the student as input and print wish message by name
def wish_student(name):
    print("Hello", name, "Good morning")

# write a function to check whether the given number is even or odd
def even_odd(number):
    if number % 2 == 0:
        print(number,"is even")
    else:
        print(number, "is Odd")

def subtraction(a,b):
    return a-b


def wish(name, message):
    print("Hello", name, message)



# wish(name="Nani", "Good morning") #SyntaxError: positional argument follows keyword argument
# def wish_message(name="guest", message="good morning"): # default arguments
#     print("Hello", name, message)

def wish_message(message, name="guest"): # default arguments
    print("Hello", name, message)


def sum_values(*n):
    print(type(n))
    total = 0
    for n1 in n:
        total += n1
    return total


def display_student_info(**kwargs):
    print(type(kwargs))
    for k,v in kwargs.items():
        print(k,v)




if __name__ == "__main__": # if this program is executed directly
    print("Functions intro __name__ is :", __name__)
    display_student_info(rno=1234, name="nani", marks=70, subject="java")

    display_student_info(rno=1234, name="Dhoni", marks=80)

    print(sum_values(10, 20))
    print(sum_values(20, 30, 40, 50, 60))
    print(sum_values(20, 30, 40, 50, 60, 780, 900))
    print(sum_values())

    wish_message("Nani", "Good morning")
    wish_message("good evening")

    wish("Nani", "Good morning")  # positional arguments
    wish(name="Nani", message="Good morning")
    wish(message="good evening", name="Nani")
    wish("good evening", "Nani")

    wish("Nani", message="Good morning")

    print(subtraction(10, 20))
    # print(subtraction(10)) # TypeError: subtraction() missing 1 required positional argument: 'b'
    print(subtraction(20, 10))

    print(subtraction(b=10, a=20))
    # print(subtraction(b=10)) # TypeError: subtraction() missing 1 required positional argument: 'a'

    wish_student("Rithwik")
    wish_student("Anjali")
    print(wish_student("Divya"))

    print(addition(10, 20))  # way to call a function
    print(addition(30, 40))
    addition(100, 200)
    sum_value = addition(300, 400)
    print(sum_value)

    even_odd(10)
    even_odd(20)
    even_odd(5)
    even_odd(9)





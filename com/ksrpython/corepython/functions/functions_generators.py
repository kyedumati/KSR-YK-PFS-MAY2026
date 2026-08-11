# it is eager and builds the whole list in memory first
squares_list = [x*x for x in range(1,11)] # 1,4,9,16,25,........
print(squares_list)
print(squares_list[0])

#
squares_gen = (x*x for x in range(1,5)) # generator
print(squares_gen)
# print(next(squares_gen)) #
# print(next(squares_gen))
# print(next(squares_gen))
# print(next(squares_gen))
# print(next(squares_gen)) # generator values will be exhausted

print(list(squares_gen)) # generator is exhausted here
# print(next(squares_gen)) #

# wap to print count down with next and function
def countdown(n):
    while n > 0:
        print("inside function")
        yield n
        n -= 1

print("before countdown")
g = countdown(10)
print("Count down over")
print(next(g))
print(next(g))
print(next(g))
print(next(g))

for value in g: #
    print(value, end=' ')

# even number stream
def even_stream(limit): # limit is something until where you want to generate even numbers
    n = 0
    while n<= limit:
         if n % 2 == 0:
             yield n
         n = n + 1

print(list(even_stream(10)))

# Wap to print ATM menu functions : show_menu(), deposit(), withdraw()
# Create @log_calls decorator print function name and arguements and duration that function takes to execute
# Write a generator fibanocci(n) yielding first n fibanocci numbers
# Wap to find longest name in students using reduce functions Ex: input: ["Ravi", "Ananya", "Ram", "Om Raut", "Prabhas"] Output: Praphas

# Write a validators for validating email, phone number and names:
# hint: is_email, is_phone_valid, is_name_valid

# Wap to check is_strong_password (leng>8, both small and upper, number, one special)
# write a decorator for checkin token is valid or not, if token is valid, allow user to sign in or signup
#hint: is_token_valid and is_otp_valid two decorators
# if token is valid-> allow him to signin : sign_in
# if otp valid --> allow him to singup


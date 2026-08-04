# create a decorator to print different wish message for if name is Sachin, without impacting existing function

def wish_decorator(func): # wish_decorator(wish(name))
    def inner(name):
        if name=="Sachin":
            print("Hello Sachin sir, good evening")
        else:
            func(name) # we are calling original function the name
    return inner # inner is decorated

# this is with decorator annotation, always decorator will be called
# @wish_decorator # decorating your function with custom decorator
# def wish(name): # orginal raw function
#     print("Good morning", name)

# without giving decorator we can independently use both the functionalities
def wish(name):
    print("Good morning", name)

wish("Kasi")
wish("Ravi")
wish("Raju")
# wish("Sachin")

decor_function = wish_decorator(wish)
decor_function("Sachin")
decor_function("Kasi")

# Write a function to view dashboard: to view the dashboard pre-requisitie is login
current_user = None

def require_login(func):
    def inner():
        if current_user is None:
            print("Please login first")
            return None
        return func()

    return inner

@require_login  # this is a decorator to check and validate if user is logged in or not
def view_dashboard():
    return "Welcome", {current_user}

@require_login
def view_reels():
    return "Enjoy watching reels", {current_user}

view_dashboard()
current_user = "Ravi"
print(view_dashboard())

print(view_reels())


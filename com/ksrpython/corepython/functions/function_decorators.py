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

# Write a function to view dashboard: to view the dashboard pre-requisite is login
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

from datetime import datetime

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        #print(func, "started at", start_time)
        func(*args, **kwargs)
        end_time = datetime.now()
        #print(func, "ends at", end_time)
        print("Time taken to execute", func.__name__, end_time - start_time)
    return wrapper


# timer decorator
@timer_decorator
def get_categories():
    print("Profile")
    print("Meta AI")
    print("Friends")
    print("Dashboard")

@timer_decorator
def get_stories():
    print("get all stories from database")

@timer_decorator
def get_advertisements():
    print("get all advertisements from database")

@timer_decorator
def friends_list_online():
    print("friends online")

get_categories()
get_stories()
get_advertisements()
friends_list_online()


# proces loan for bank for multiple people at a time
bank_account_list = [
    { "name": "kasi",
      "accountno": "123"
    },
    {"name": "ravi",
     "accountno": "222"
     },
    {"name": "virat",
     "accountno": "333"
     }
]

for bank_account in bank_account_list:
    print("process loan for ", bank_account.get("name"))
    bank_account["balance"] = 1000.00

print(bank_account_list)

def mygenerator():
    yield "a"
    yield "b"
    yield "c"

g = mygenerator()
print(type(g))
print(next(g))
print(next(g))
# print(next(g))
# print(next(g))

# print a countdown
# def countdown(num):
#     print("start countdown")
#     while num > 0:
#         print("iteration for", num)
#         num -= 1
#         yield num
#         num -= 1

values = countdown(5)
print("countdown is called")
print("countdown is called lin2")
print("countdown is called lin3")
# print(next(values))
# print(next(values))
print(type(values))
print(list(values))
for value in values:
    print(value)



# bool
print(bool(0))
print(bool(1))
print(bool(20)) # any non-zero in int form will become True
# float values
print(bool(3.147))
print(bool(0.0)) # False
print(bool(0.1)) # True

print(bool(1+5j))
print(bool(0+0j))
print(bool(10+0j))

print(bool("kasi"))
print(bool("True"))
print(bool('')) # empty string
print(bool(' '))

first_name = "kasi"
email = ""
if first_name:
    print("First is name ", first_name)
else:
    print("First name is empty, please enter firstname")


if email:
    print("Email is ", email)
else:
    print("Email is empty, please enter email")
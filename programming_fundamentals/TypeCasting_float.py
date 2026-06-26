# float() is used to convert any other type to float
from DataTypes import is_eligible

a = 123  # int form
print(float(a))
complex_value = 12 + 5j
# print(float(complex_value)) # TypeError: float() argument must be a string or a real number, not 'complex'
status = True
# print(status)
print(type(status))
print(float(status))
is_eligible = False
print(type(is_eligible))
print(float(is_eligible))

# print(float("kasi")) # ValueError: could not convert string to float: 'kasi'
print(float("3.147"))
print(float("3345"))

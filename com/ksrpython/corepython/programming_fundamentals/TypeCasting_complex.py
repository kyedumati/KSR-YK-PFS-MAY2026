# complex()
print(complex(234)) # real part and imaginary part
print(complex(234, 4))
print(complex(234.5))
print(complex(True)) # 1 + 0j
print(complex(False)) # 0j
# print(complex("kasi")) # ValueError: complex() arg is a malformed string
print(complex("10.5"))

# I want to give real part as 20 imaginary part has 40 to complex fuction in the string form
# print(complex("20", "40")) # TypeError: complex() argument 'real' must be a real number, not str
print(complex(20, 40))
print(complex(True, False))
print(complex(False, True))
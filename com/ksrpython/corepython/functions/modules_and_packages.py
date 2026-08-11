#import functions_intro as fi  # import everything from this module
from functions_intro import display_student_info, addition  # import only display_student_inf and addtion functions from fucntions_intro module
# from functions_intro import *
# import functions_intro2 as fi2, functions_intro as fi3
# import functions_intro2
# from functions_intro import display_student_info as ds
# fi.display_student_info(rno=1234, name="Module Test", marks=70, subject="java")
# print(fi.addition(30,40))
from math import sqrt, ceil, floor
from ksrpython.test import test_package
from operators.operators_assignment import *

print(sqrt(2))
print(sqrt(16))
print(ceil(10.1))
print(floor(10.6))

display_student_info(rno=1234, name="Module Test", marks=70, subject="java")
print(addition(30,40))
print(test_package())


# print(dir(functions_intro2))
# print(dir())
# print(__builtins__)
# print(__name__) # im printing current module(module_packages) name variable value
# print(__doc__)
# print(__cached__)
# print(dir(functions_intro))
# print(functions_intro.__name__) # im printing functions_intro module __name__ variable value

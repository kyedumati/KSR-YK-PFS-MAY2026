# bytes
marks = bytes([60,50,70,80])
print(type(marks))
print(marks)
print(marks[1])
print(marks[-2])
# print(marks[8])
# intermediate_marks = bytes([345, 670, 986, 998])  #1000
# print(type(intermediate_marks))
# bytes[1] = 90 # change or modify the value at position or index 1
print(marks)

# bytearray
ssc_marks = bytearray([65,55,76,84])
print(ssc_marks[1])
print(ssc_marks[-2])
ssc_marks[1] = 95
print(ssc_marks[1])
for mark in ssc_marks:
    print(mark)
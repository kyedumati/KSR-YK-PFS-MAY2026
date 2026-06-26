# range
r = range(12)
print(r)
for i in r:
    print(i)

range_values = range(10, 20)
print(range_values)
for i in range_values:
    print(i)

incrment_values = range(10, 20, 2) # 10 12 14 16 18
print(incrment_values)
for i in incrment_values:
    print(i)

incrment_values2 = range(100, 120, 5) # 100 105 110 115
# print(incrment_values2)
# for i in incrment_values2:
#     print(i)
print(incrment_values2[2])
# print(incrment_values2[9])  # IndexError
incrment_values2[2] = 120 # TypeError: 'range' object does not support item assignment


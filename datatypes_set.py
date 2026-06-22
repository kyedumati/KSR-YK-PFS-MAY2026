# set datatype
fruits_set = {'apple', 'banana', 'orange'}
print(fruits_set)
print(type(fruits_set))
# print(fruits_set[1]) # TypeError: 'set' object is not subscriptable
fruits_set.add('grape')
print(fruits_set)
fruits_set.remove('orange')
print(fruits_set)

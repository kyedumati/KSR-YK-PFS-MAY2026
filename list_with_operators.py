a = [10,20,30]
b = [50,60,70]
# a.extend(b)
# print(a)

c= a+b
print(c)
d =4
# c = c+d # TypeError: can only concatenate list (not "int") to list
c = c*d
print(c)

x = ["Dog", "Cat", "Rat"]
y = ["Dog", "Cat", "Rat"]
z = ["DOG", "CAT", "RAT"]
print(x==y)
print(x==z)
print("horse" in x) # if horse is there in x it will return True
print("Dog" in x)
print("horse" not in x) # if horse is there in x it will return True
print("Dog" not in x)

# clear() --> to remove all elements in the list
x.clear()
print(x)

# nested list:
n = [[1,2,3],[4,5,6],[7,8,9], [10,[11,12]]]
print(n[1])
nested_list_1 = n[1] # [4,5,6]
print(nested_list_1[1])
print(n[1][1])
# print 9 from n
print(n[2][2])
# print 7 from n
print(n[2][0])
#print 12 from n
print(n[3][1][1])
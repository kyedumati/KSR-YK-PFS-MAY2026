s = {10,20,30,30}
print(s)
print(type(s))
s2 = {}
print(s2)
print(type(s2))

print(set(range(10)))
print(set([10,10,20,30,30,40,40,50]))
s.add(1245)
print(s)
s.update({1,2,3,4}, [10,20,400,500])
print(s)
print(id(s))
s3 = s.copy()
print(s3)
print(id(s3))
print(s3.pop())
print(s3)
print(s3.pop())
print(s3)
print(s3.remove(1245))
print(s3)
# print(s3.remove(1245)) # KeyError: 1245
print(s3.discard(1245))

x = {10,20,30,40}
y = {30,40,50,60}
print(x.union(y))
print(x|y)
print(x.intersection(y))
print(x&y)
print(x.difference(y))
print(y.difference(x))
print(x.symmetric_difference(y))

# set comprehension
s = {x**2 for x in range(10)}
print(s)
print(type(s))
# print(s[2]) # TypeError: 'set' object is not subscriptable

# To build a college event registration system
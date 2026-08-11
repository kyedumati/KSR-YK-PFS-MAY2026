print("Before empty line")
print()
print("After empty line", end="\t")
a,b = 10, 20
print(a,b)

print("Virat \nKohli")
x= 100
y= 200
print(x,y, sep="___")
# Form3: print with variable number arguments
print("x and y values are: ", x, y, sep="Kasi")
# form4: print with end param
print("virat Kohli", end='\n')
print("Kasi yedumati")

# form5: print wiht object
students = ["kasi", "virat", "dhoni"]
print(students)
t= (10,20,30)
print(t)

# form6: mixing variables with string in the output
course = "python full stack"
duration = 5
trainer = "kasi"
# I'm attending Kasi's full stack python course, duration is 5 months
print("I'm attending", trainer,"'s", course,",", "duration is", duration, "months", sep=" ")

# form7: formatted string
print("I'm attending %s's %s course, duration is %d months"%(trainer,course,duration))
print("python class student are %s"%(students))

# form8 with replacement operator {}
print("I'm attending {1}'s {0} course, duration is {2} months".format(course, trainer,duration))


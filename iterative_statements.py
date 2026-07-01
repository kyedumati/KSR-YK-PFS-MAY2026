emp_salaries = [1000, 2000, 3000, 2400,3000, 4000, 50000, 60000]
print("Before bonus:", emp_salaries)
# emp_salaries[0] += 100000
# emp_salaries[1] += 100000
# emp_salaries[2] += 100000
# emp_salaries[3] += 100000
for salary in emp_salaries: # salary is a variable which holds single value in every iteration
    salary += 100000
    print(salary)
# print("After bonus: ", emp_salaries)

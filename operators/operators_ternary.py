
# ternary operator
# x = firstValue if condition else secondValue
# Write a program to take two variable with numbers and print the maximum value
a = 500
b = 60
max_value = a if a > b else b
print(max_value)

# write a program to take two variables with numbers and print the minimum value
x = 60
y = 90
min_value = x if x < y else y
print(min_value)

# write a program to check if voter applicant is eligible or not
# condition1 : age should be greater than 18        : age>=18
# condition2 : he should belong to state Telangana  : state == "Telangana"
candidate_age = 20
candiate_state = "AP"
name = "Kasi Yedumati"
eligibility_check_statement = ''
# eligibility_check_statement = " is Eligble for Vote" if candidate_age>=18 and candiate_state == "Telangana" else " is not Eligble for Vote"
if candidate_age>=18 and candiate_state.strip().upper() == "TELANGANA":
    eligibility_check_statement = "is Eligble for Vote"
else:
    eligibility_check_statement = "is Not Eligible"
print(name, eligibility_check_statement)

# Write a program to find minimum of 3numbers
a = 1
b = 5
c = 3
min_value = a if (a<b and a<c) else (b if b<c else c)
print(min_value)

# Assignment: Write a program to find maximum of 3 numbers

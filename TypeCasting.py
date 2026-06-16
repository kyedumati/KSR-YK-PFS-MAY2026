bank_balance = "1000"
deposit = "200"
print(type(bank_balance))
print(type(deposit))

bank_balance = int(bank_balance) # converting and reinitalising the value to bank_b alance
deposit = int(deposit)

print(type(bank_balance))
print(type(deposit))

final_balance = bank_balance + deposit
print(final_balance)

# float, complex, bool
marks_percentage = 97.658998
marks_percentage = int(marks_percentage)
print(marks_percentage)
complex_value = 10+5j
# print(int(complex_value)) # complex values cannot be converted to int
iphone_price = 125234.56
print(int(iphone_price))

status = True # boolean datatype
print(int(status))
is_customer_active = False # bool
print(int(is_customer_active))

first_name = "kasi"
last_name = "yedumati"
# print(int(first_name)) # ValueError: invalid literal for int() with base 10: 'kasi'
print(int("10.5")) # ValueError: invalid literal for int() with base 10: '10.5'







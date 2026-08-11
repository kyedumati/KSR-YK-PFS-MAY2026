# Problem Statement
'''
A student wants to register for your python course
accept/ask:
Full name
emailid
mobile number
password
'''
print("="* 60)
print("Welcome to KSR Python full stack program registration")
print("="* 60)
# Step1- accept inputs
name = input("Please enter your name: ")
email = input("Please enter your email: ")
password = input("Please enter your password: ")
mobile = input("Please enter your mobile number: ")

print()
# Step2: we have to sanitize, massage and validate the data before performating any operations
massaged_name = name.strip().title() #   kasi yeduMAti   -->Kasi Yedumati
massaged_email = email.strip()
massaged_password = password.strip()
massaged_mobile = mobile.strip()

#Step3: Validate the data
# if not name.isalpha():
#    print("Please enter a valid name")
# else:
#    print("Name is valid")
# valid_domains = ['.com', '.edu']

firstname = massaged_name.split()[0]
lastname = massaged_name.split()[1]
valid_name = firstname.isalpha() and lastname.isalpha()

valid_email = '@' in massaged_email and (massaged_email.endswith(".com") or massaged_email.endswith(".edu"))
# alphabets, numbers, special characters and length >=8
valid_password = len(massaged_password) >=8 and massaged_password.isalnum()
valid_mobil = len(massaged_mobile) == 10 and massaged_mobile.isdigit() # 123456

masked_mobile = "*******" + massaged_mobile[-4:]

print("="*60)
print("Validation report")
print("="*60)
if valid_name:
    print("Name is valid")
else:
    print("Name is invalid")

if valid_email:
    print("Email is valid")
else:
    print("Email is invalid")

if valid_password:
    print("Password is valid")
else:
    print("Password is invalid, enter alphasenumberic value contains atleast 8 length")

if valid_mobil:
    print("Mobile number is valid")
else:
    print("Mobile number is invalid")

if valid_mobil and valid_email and valid_password and valid_name:
    print("Regirstration is successfulll")
    # we will write the data to database
else:
    print("Registration is failed")
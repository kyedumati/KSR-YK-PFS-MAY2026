import bcrypt

password = "Acme@1234"

print(password.encode()) # converting string to bytes

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) # decode is converting bytes to string
print(hashed)
print(len(hashed))

user_input = "Acme@1234"
print(bcrypt.checkpw(user_input.encode(), hashed))
user_input = "acme@1234"
print(bcrypt.checkpw(user_input.encode(), hashed))

# PHI  --> Patient/Protected Health information --> diabates/heart/sexual healths
# PII  --> Patient identity information         --> address, name


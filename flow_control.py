# 1. take the iformation from the use
# 2. sanitise the data
# 3. validate if custome is eligible
# 4. insert the data into the database
# 5. issue the voter card
# 6. reject with error message saying, customer is not eligible
user_input_cricketer = input("Who is the odi top cricketer/batsman? ")
top_odi_batsman = "virat kohli"
if user_input_cricketer == top_odi_batsman: # True or False
    print("your answer is correct") # inside condition
    print("top odi batasman is virat")
else:
    print("your answer is incorrect")
print("End of the program") # outside if condition
emp_data ={1234: "kasi", 1122: "raju", 1123: "Ravi"}
print(emp_data[1234])
print(emp_data[1123])

contact_info = {"kasi": 99876543, "anjali": 45678, "nag":12345}
print(contact_info["kasi"])
# print(contact_info["bhuvan"]) # KeyError: 'bhuvan'
# print(contact_info.has_key("bhuvan"))
if "bhuvan" in contact_info:
    print(contact_info["bhuvan"])
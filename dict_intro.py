emp_data ={1234: "kasi", 1122: "raju", 1123: "Ravi"}
# emp_data2 ={"kasi":1234, "kasi": 2233}
# print(emp_data2)
print(emp_data[1234])
print(emp_data[1123])

contact_info = {"kasi": 99876543, "anjali": 45678, "nag":12345}
print(contact_info["kasi"])
# print(contact_info["bhuvan"]) # KeyError: 'bhuvan'
# print(contact_info.has_key("bhuvan"))
if "bhuvan" in contact_info:
    print(contact_info["bhuvan"])

print(contact_info.get("bhuvan"))
# print(contact_info["bhuvan"])
print(contact_info.get("kasi")) #getting value by key

print(contact_info.get("bhuvan", 11111))
print(contact_info.get("kasi", 1122233))
print(contact_info)
print(contact_info.get("Varshith", "Not Available"))
contact_info["kasi"] = 6302193992
contact_info["bhuvan"] = 98765432
print(contact_info)
print(len(contact_info))
del contact_info["nag"]
print(contact_info)
if "divya" in contact_info:
    del contact_info["divya"] # KeyError: 'divya'

# contact_info.clear()
# print(contact_info)
# del contact_info # deletes entire dict
# print(contact_info)

print(len(contact_info))
print(contact_info.pop("kasi"))
print(contact_info)
# print(contact_info.popitem())
# print(contact_info)

print(contact_info.keys())
print(contact_info.values())
for key in contact_info.keys():
    print(key)

for value in contact_info.values():
    print(value)

print(contact_info.items())
for key, value in contact_info.items(): #
    print(key, value)

contact_info_bkup = contact_info.copy()
print(contact_info_bkup)
print(id(contact_info_bkup))
print(id(contact_info))

# contact_info["kasi"] = 6456789
contact_info.setdefault("kasi", 99876543)
print(contact_info)
contact_info.setdefault("bhuvan", 45678)
print(contact_info)

contact_info.update({"chandu": 112233, "rithwik": "223344"})
print(contact_info)

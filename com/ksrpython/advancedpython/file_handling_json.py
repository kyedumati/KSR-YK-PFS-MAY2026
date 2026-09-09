import json

# with open("data/expenses_config.json", "r") as read_file:
#     loaded_dict = json.load(read_file)
#     print(loaded_dict)
#     print(loaded_dict.get("categories"))
#     print(loaded_dict.get("categories")[3])
#     print(loaded_dict.get("max_daily_limit"))

payment_gateway_config = {
    "payment_gateway_name": "Razorpay",
    "payment_gateway_email": "test@gmail.com",
    "payment_gateway_url": "https://razorpay.com",
    "payment_gateway_client_id": "123456",
}

with open("example_config.json", "w") as file:
    json.dump(payment_gateway_config, file, indent=2)


json_string = '{"name":"Kasi", "email":"", "url":"https://razorpay.com"}'
print(type(json_string))
loaded_json = json.loads(json_string)
print(type(loaded_json))
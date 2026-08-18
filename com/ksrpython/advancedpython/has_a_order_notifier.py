# Send a notification once the order is placed

class SmsNotification:
    @staticmethod
    def send_sms_notification(order_meesage):
        print("Order sent:" + order_meesage)


class OrderService:
    def __init__(self, order_id, product_name):
        self.order_id = order_id
        self.product_name = product_name

    def place_order(self):
        # print("Order placed:"+self.order_id + "Product:"+ self.product_name)
        SmsNotification.send_sms_notification("Order placed:"+self.order_id + "Product:"+ self.product_name) # HAS-A relationship

order1 = OrderService("1234", "iphone")
order1.place_order()

class GstUtility:
    @staticmethod
    def gst_amount(amount, rate=0.18):  # static utility
        return amount * rate

class Order:

    orders_count = 0 # static variable

    def __init__(self, product, price, quantity):
        self.product = product
        self.price = price
        self.quantity = quantity
        Order.orders_count += 1


    def get_order_total(self):
        return self.price * self.quantity

    @classmethod
    def get_order_count(cls):
        return cls.orders_count

    # @staticmethod
    # def gst_amount(amount, rate = 0.18): # static utility
    #     print(Order.orders_count)
    #     return amount * rate


# passing members of one class to another class
class Discount:
    @staticmethod
    def apply_discount(order: Order):
        return order.get_order_total() - order.get_order_total()/20




order1 = Order("iphone", 120000, 2)
total_amount = order1.get_order_total()
# include_gst_total = total_amount + GstUtility.gst_amount(total_amount)
# order1.include_gst_total = include_gst_total
print("Total bill for order1 before discount: ", total_amount + GstUtility.gst_amount(total_amount))
print("Total bill for order1: after discount: ",Discount.apply_discount(order1))


order2 = Order("macbook", 200000, 3)
order2_total = order2.get_order_total()
print("Total bill for order2: ", order2_total + GstUtility.gst_amount(order2_total))

print("Total orders are: ", Order.get_order_count())

# Order.gst_amount(12000)














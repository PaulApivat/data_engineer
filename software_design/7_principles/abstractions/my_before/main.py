from pos.order import Order
from pos.payment import PaymentProcessor 
from pos.authorization import authorize_sms, authorize_google

""" First Abstraction: 
- remove dependency between specific authorization functions and payment processor 
- use type definition to provide this separation 

- main(): 
    - no longer passing string "sms" in PaymentProcessor class, 
    - but passing authorize_sms which is a reference to the authorize_sms() function 
    - instead of PaymentProcessor, main() is not determining which authorization function is passed

"""

def main():
    order = Order()
    order.add_item("Keyboard", 1, 5000)
    order.add_item("SSD", 1, 15000)
    order.add_item("USB cable", 2, 500)

    print(f"The total price is: ${(order.total_price / 100):.2f}.")
    processor = PaymentProcessor(authorize_sms)
    processor.pay_credit(order, "123456")


if __name__ == "__main__":
    main()

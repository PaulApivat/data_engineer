"""
The Order class is doing too much. It has to add items AND pay for them.
1st: Increasing Order (class) Cohesion
2nd: Increasing PaymentProcessor (class) Cohesion
1st Solution: Separate pay function into PaymentProcessor class.
    - need to make Order class a parameter for PaymentProcessor.
    - add set_status function in Order class to cleaning set status
2nd Solution: Separate debit & credit payment into two functions within PaymentProcessor class
    - change Order status attribute from string -> Enum type
"""
from enum import Enum, auto


class OrderStatus(Enum):
    OPEN = auto()
    PAID = auto()


class Order:
    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[int] = []
        self.status: OrderStatus = OrderStatus.OPEN

    def add_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def set_status(self, status: OrderStatus) -> None:
        self.status = status


class PaymentProcessor:
    def pay_debit(self, order: Order, security_code: str) -> None:
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.set_status(OrderStatus.PAID)

    def pay_credit(self, order: Order, security_code: str) -> None:
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.set_status(OrderStatus.PAID)


def main() -> None:
    order = Order()
    order.add_item("Keyboard", 1, 5000)
    order.add_item("SSD", 1, 15000)
    order.add_item("USB cable", 2, 500)

    processor = PaymentProcessor()
    processor.pay_debit(order, "0372846")


if __name__ == "__main__":
    main()

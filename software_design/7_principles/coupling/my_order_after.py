from enum import Enum, auto

""" 
Law of Demeter
Content Coupling: add_item() uses Order instance as a params and changes attribute of Order
    - problem: add_item() uses Order class and changes its attributes 
    - solution: make add_item() part of Order class
    - problem: compute_total_price() also uses Order class and print 
        total price w/o returning it so coupled to "output" system
    - solution: make compute_total_price part of Order class and 
        move print statement to main() to de-couple function from output system

"""


class PaymentStatus(Enum):
    """Payment status"""

    OPEN = auto()
    PAID = auto()


class Order:
    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[int] = []
        self.status: str = "open"


    def add_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    @property
    def total_price(self) -> int:
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total
        


def main() -> None:
    order = Order()
    # add_item is now part of Order class
    order.add_item("Keyboard", 1, 5000)
    order.add_item("SSD", 1, 15000)
    order.add_item("USB cable", 2, 500)

    print(f"The total price is: ${(order.total_price / 100):.2f}.")


if __name__ == "__main__":
    main()
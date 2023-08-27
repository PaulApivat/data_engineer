from enum import Enum, auto
from dataclasses import dataclass, field


class PaymentStatus(Enum):
    """Payment status"""

    OPEN = auto()
    PAID = auto()

@dataclass 
class EachItem:
    item: str 
    quantity: int 
    price: int 

    @property 
    def total_price(self) -> int: 
        return self.quantity * self.price 

@dataclass 
class Order:
    items: list[EachItem] = field(default_factory=list)
    status: PaymentStatus = PaymentStatus.OPEN

    def add_item(self, item: EachItem) -> None:
        self.items.append(item)

    @property
    def total_price(self) -> int:
        return sum(item.total_price for item in self.items)

def main() -> None:
    order_data = Order()
    order_data.add_item(EachItem("Keyboard", 1, 5000))
    order_data.add_item(EachItem("SSD", 1, 15000))
    order_data.add_item(EachItem("USB cable", 2, 500))

    print(f"The total price is: ${(order_data.total_price / 100):.2f}.")


if __name__ == "__main__":
    main()



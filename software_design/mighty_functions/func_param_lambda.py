from dataclasses import dataclass
from typing import Callable
from functools import partial


@dataclass
class Customer:
    name: str
    age: int


def send_email_promotion(
    customers: list[Customer], is_eligible: Callable[[Customer], bool]
) -> None:
    """Higher order function accepts function as argument."""
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible")
        else:
            print(f"{customer.name} is not eligible for promotion.")


# demonstrate closures and higher-order function
def is_eligible_for_promotion(cutoff_age: int = 50) -> Callable[[Customer], bool]:
    """Defining a function inside another function is a Closure."""

    def is_eligible(customer: Customer) -> bool:
        return customer.age >= cutoff_age

    return is_eligible


# simpler version: Partial functions
def is_eligible_for_promotion_simple(customer: Customer, cutoff_age: int = 50) -> bool:
    return customer.age >= cutoff_age


def main() -> None:
    customers = [
        Customer("Alice", 25),
        Customer("Bob", 30),
        Customer("Charlie", 35),
        Customer("David", 40),
        Customer("Eve", 45),
        Customer("Frank", 50),
        Customer("Grace", 55),
        Customer("Holly", 60),
        Customer("Iris", 65),
    ]
    send_email_promotion(customers, is_eligible_for_promotion(30))
    print("----Example use of lambda function -----")
    send_email_promotion(customers, lambda customer: customer.age >= 50)
    print("----Example of Partial functions")
    is_eligible = partial(is_eligible_for_promotion_simple, cutoff_age=25)
    send_email_promotion(customers, is_eligible)


if __name__ == "__main__":
    main()

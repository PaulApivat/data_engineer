# Violations of type hints ignored by the Python interpreter
from typing import Callable
from enum import Enum, auto

IntFunction = Callable[[int], int]


class Book:
    def __init__(self, author: str, title: str, pages: int) -> None:
        self.author = author
        self.title = title
        self.pages = pages

    def __len__(self):
        return self.pages


class Month(Enum):
    """Enum are good tools to reprsent a limited set of options, instead of strings"""

    JANUARY = auto()
    FEBRUARY = auto()
    MARCH = auto()
    APRIL = auto()
    MAY = auto()
    JUNE = auto()
    JULY = auto()
    AUGUST = auto()
    SEPTEMBER = auto()
    OCTOBER = auto()
    NOVERMBER = auto()
    DECEMBER = auto()


def compute_stats(users, plans, products):
    # code here
    pass


def multiply_by_two(x: float) -> float:
    return x * 2.0


def add_three(x: int) -> int:
    return x + 3


# string in def is_birthday(month: str): is not strict enough, better use Enum which gives better type hints
def is_birthday(month: Month):
    return month == Month.JUNE


def birthday_month_year() -> tuple[Month, int]:
    return Month.APRIL, 1981


def main():
    """Description: Example of Duck Typing
    The len() function can be called on a string, list, dict or even class
    regardless of their type.

    As long as the structure of the objct adheres to the protocol,
    Python favoring Structural Typing over Nominal Typing,

    As long as the object adheres to the protocol that it has a 'len()' function,
    then it can be called on different types of input (also related to Dynamically Typed)

    """
    my_str = "Hi this is also a string"
    print(len(my_str))
    print("this" in my_str)
    print("slicing ", my_str[1:6])
    amount: int = 30000
    formatted_str = f"The amount is ${amount / 100:.2f}"
    print(formatted_str)
    my_list = [34, 54, 65, 78]
    print(len(my_list))
    my_dict = {"one": 123, "two": 456, "three": 789}
    print(len(my_dict))
    my_book = Book("Robert Martin", "Clean Code", 464)
    print(len(my_book))
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    print(is_birthday(months[4]))
    print(is_birthday(Month.JUNE))
    my_month, my_year = birthday_month_year()
    print(my_month)
    print(my_year)
    print(birthday_month_year())
    print(type(3 + 4.5))
    my_list = [0, 2, 4, 6, 7, 5]
    new_list = my_list[4:] + my_list[:2]
    print(new_list)

    # demonstrating pylance
    # my_var: IntFunction = multiply_by_two
    # print(my_var(5))


if __name__ == "__main__":
    main()

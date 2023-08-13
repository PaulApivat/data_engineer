# Violations of type hints ignored by the Python interpreter
from typing import Callable

IntFunction = Callable[[int], int]


class Book:
    def __init__(self, author: str, title: str, pages: int) -> None:
        self.author = author
        self.title = title
        self.pages = pages

    def __len__(self):
        return self.pages


def compute_stats(users, plans, products):
    # code here
    pass


def multiply_by_two(x: float) -> float:
    return x * 2.0


def add_three(x: int) -> int:
    return x + 3


def main():
    """Description: Example of Duck Typing
    The len() function can be called on a string, list, dict or even class
    regardless of their type.

    As long as the structure of the objct adheres to the protocol,
    Python favoring Structural Typing over Nominal Typing,

    As long as the object adheres to the protocol that it has a 'len()' function,
    then it can be called on different types of input (also related to Dynamically Typed)

    """
    my_str = "hello"
    print(len(my_str))
    my_list = [34, 54, 65, 78]
    print(len(my_list))
    my_dict = {"one": 123, "two": 456, "three": 789}
    print(len(my_dict))
    my_book = Book("Robert Martin", "Clean Code", 464)
    print(len(my_book))

    # demonstrating pylance
    # my_var: IntFunction = multiply_by_two
    # print(my_var(5))


if __name__ == "__main__":
    main()

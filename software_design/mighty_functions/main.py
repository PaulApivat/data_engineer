from typing import Any

CUSTOMERS = {
    "Alice": {"phone": "2341", "credit_card": "2341"},
    "Bob": {"phone": "9102", "credit_card": "5342"},
}


class MyClass:
    def __init__(self, x: int) -> None:
        self.x = x

    def __call__(self):
        return self.x


def pure_function(x: int, y: int) -> int:
    return x + y


def side_effect_function() -> None:
    """Function that changes something outside of it's scope has a side-effect.
    Hard to test, generally try to avoid.
    """
    CUSTOMERS["Alice"]["phone"] = "1234"


def side_effect_into_pure_function(customers: dict[str, Any]) -> None:
    """Turning side-effects into pure function by supply dependency as argument instead of letting
    the function change an external value itself;

    - Avoiding side-effects by not changing a variable directly
    """
    customers["Alice"]["phone"] = "1234"


def main() -> None:
    obj = MyClass(12)
    print(CUSTOMERS)
    print(pure_function(1, 2))
    print(pure_function.__call__(1, 2))
    print(obj.x)
    print(obj.__call__())
    print(obj())
    print((2).__class__)


if __name__ == "__main__":
    main()

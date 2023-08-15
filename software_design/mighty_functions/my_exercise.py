import random
import string
from datetime import datetime
from functools import partial
from typing import Callable

# a) Both generate_id and weekday are not pure functions.
#    Why not? How would you write tests for these functions?

SelectionFn = Callable[[], str]


def generate_id(length: int, sel_fn: SelectionFn) -> str:
    return "".join(sel_fn() for _ in range(length))

    # return "".join(
    #    random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    # )


def weekday(date: datetime) -> str:
    # today = datetime.today()
    return f"{date:%A}"


# Turn side-effects into pure functions by moving dependencies and supplying them as arguments down here
# instead of letting the function change them.
def main() -> None:
    print(f"Today is a {weekday(datetime.today())}")
    sel_fn: SelectionFn = partial(
        random.choice, seq=string.ascii_uppercase + string.digits
    )  # type: ignore
    print(f"Your id = {generate_id(10, sel_fn)}")


if __name__ == "__main__":
    main()

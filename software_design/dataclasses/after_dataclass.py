import random
import string
from datetime import datetime
from enum import Enum, auto
from dataclasses import dataclass, field

"""
@dataclasses provides a representation of more "data-oriented" classes
    while removing boiler-plate associated with normal "classes".
    A normal class might have a few data attributes, but many methods
    but a dataclass might have more data attributes. 

Once you put @dataclass above a class, you can use its features like:
- u can define attributes once, and @dataclass will generate the initializer for you

@dataclasses don't allow mutable objects (list) for instance variable defaults,
- must use 'default_factory'
"""


def generate_vehicle_license() -> str:
    """Helper method for generating a vehicle license number."""

    digit_part = "".join(random.choices(string.digits, k=2))
    letter_part_1 = "".join(random.choices(string.ascii_uppercase, k=2))
    letter_part_2 = "".join(random.choices(string.ascii_uppercase, k=2))
    return f"{letter_part_1}-{digit_part}-{letter_part_2}"


class Accessory(Enum):
    AIRCO = auto()
    CRUISECONTROL = auto()
    NAVIGATION = auto()
    OPENROOF = auto()
    BATHTUB = auto()
    MINIBAR = auto()


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


def default_accessories():
    return [Accessory.AIRCO, Accessory.NAVIGATION]


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    license_plate: str = field(default_factory=generate_vehicle_license, init=False)
    accessories: list[Accessory] = field(default_factory=default_accessories)
    fuel_type: FuelType = FuelType.ELECTRIC

    def __post_init__(self):
        """Another way of setting default values for a dataclass"""
        self.license_plate = generate_vehicle_license()
        if self.brand == "Tesla":
            self.license_plate += "-t"

    def generate_vehicle_license(self):
        self.license_plate = generate_vehicle_license()

    def reserve(self, date: datetime):
        print(f"Vehicle is reserved for {date}.")


def main() -> None:
    """
    Create some vehichles and print their details
    """

    tesla = Vehicle(
        brand="Tesla",
        model="Model 3",
        color="black",
        # license_plate=generate_vehicle_license(),
        accessories=[
            Accessory.AIRCO,
            Accessory.MINIBAR,
            Accessory.NAVIGATION,
            Accessory.CRUISECONTROL,
        ],
    )

    volkswagen = Vehicle(
        brand="Volkswagen",
        model="ID3",
        color="white",
        # license_plate=generate_vehicle_license(),
        # accessories=[Accessory.AIRCO, Accessory.NAVIGATION],
    )

    bmw = Vehicle(
        brand="BMW",
        model="520e",
        color="blue",
        # license_plate=generate_vehicle_license(),
        # license_plate="FAKE LICENSE", <----- init=False; license_plate: str = field(default_factory=generate_vehicle_license, init=False)
        fuel_type=FuelType.PETROL,
        # accessories=[Accessory.NAVIGATION, Accessory.CRUISECONTROL],
    )

    print(tesla)
    print(volkswagen)
    print(bmw)


if __name__ == "__main__":
    main()

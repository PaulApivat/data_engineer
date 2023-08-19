from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


class TruckCabStyle(Enum):
    REGULAR = auto()
    EXTENDED = auto()
    CREW = auto()


@dataclass
class PriceSource(Protocol):
    def compute_price(self) -> int:
        ...


@dataclass
class DistancePricing:
    price_per_km: int

    def compute_price(self) -> int:
        return int(self.price_per_km)


@dataclass
class DailyPricing:
    price_per_day: int

    def compute_price(self) -> int:
        return int(self.price_per_day)


@dataclass
class MonthlyPricing:
    price_per_month: int

    def compute_price(self) -> int:
        return int(self.price_per_month)


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    fuel_type: FuelType
    license_plate: str
    reserved: bool
    number_of_seats: int
    storage_capacity_litres: int
    price_sources: list[PriceSource] = field(default_factory=list)

    def add_price_source(self, price_source: PriceSource):
        self.price_sources.append(price_source)

    def compute_price(self) -> int:
        return sum(source.compute_price() for source in self.price_sources)


def main():
    ford = Vehicle(
        brand="Ford",
        model="Fiesta",
        color="red",
        fuel_type=FuelType.PETROL,
        license_plate="ABC-123",
        reserved=False,
        number_of_seats=5,
        storage_capacity_litres=300,
    )
    ford.add_price_source(DistancePricing(price_per_km=10))
    ford.add_price_source(DailyPricing(price_per_day=50))
    print(ford)

    tesla = Vehicle(
        brand="Tesla",
        model="Model 3",
        color="black",
        fuel_type=FuelType.ELECTRIC,
        license_plate="DEF-456",
        reserved=False,
        # price_per_month=1000,
        number_of_seats=5,
        storage_capacity_litres=300,
    )
    tesla.add_price_source(MonthlyPricing(price_per_month=1000))
    tesla.add_price_source(DailyPricing(price_per_day=75))
    print(tesla)

    # Unfortunately, the current setup makes it impossible to
    # rent the Tesla per day since it only has a price per month.
    # The same goes for the Ford, it can only be rented per day and
    # not per month (at least not easily).
    # In this exercise, you will have to refactor the code to make
    # it possible to rent both cars per day and per month, by using
    # composition over inheritance.


if __name__ == "__main__":
    main()

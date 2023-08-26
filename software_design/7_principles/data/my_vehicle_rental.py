from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from reader import read_kms_to_drive, read_rent_days, read_vehicle_type

""" Start with the Data

Removing Coupling from the Main Function
- separate Customer into it's own class 
- add total_price @property to RentalContract class (reference total_price method in Vehicle class)

Improving Object Communication

** Information Expert Principle: Keep your methods close to the Data ** 
- There are 3 Levels: main(), RentalContract and Vehicle
    - at each level, the total_price() method has the information it needs
    - each level doesn't need to know the implementation details of the other levels
    - total_price() is part of Vehicle class and accesses its instance variables
    - RentalContract doesn't need to know implementation details of Vehicle class, 
        so it just calls the total_price() method of the Vehicle class and passes it's own 'days' and 'additional_km' 
    - main() function also doesn't need to know implementation details of RentalContract 
        because it just calls total_price @property RentalContract 
- By making sure that methods are close to the data, 

- Next steps: Turn RentalContract into a protocol with total_price() anything with total_price() can be rented. 
"""

FREE_KMS = 100


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    fuel_type: FuelType
    license_plate: str
    price_per_km: int
    price_per_day: int
    reserved: bool

    def total_price(self, days: int, additional_km: int) -> int:
        return days * self.price_per_day + additional_km * self.price_per_km


class ContractStatus(Enum):
    ORDERED = auto()
    PAID = auto()
    PICKED_UP = auto()
    DROPPED_OFF = auto()
    CANCELLED = auto()


@dataclass 
class Customer:
    id: int
    name: str
    address: str
    postal_code: str
    city: str
    email: str

@dataclass
class RentalContract:
    vehicle: Vehicle
    customer: Customer
    contract_status: ContractStatus
    pickup_date: datetime
    days: int = 1
    additional_km: int = 0

    @property
    def total_price(self) -> int: 
        return self.vehicle.total_price(self.days, self.additional_km)


VEHICLES = {
    "vw": Vehicle(
        "Volkswagen", "Golf", "black", FuelType.PETROL, "ABC123", 30, 6000, False
    ),
    "bmw": Vehicle("BMW", "X5", "green", FuelType.PETROL, "ABC123", 30, 8500, False),
    "ford": Vehicle(
        "Ford", "Fiesta", "white", FuelType.PETROL, "ABC123", 30, 12000, False
    ),
}

customer = Customer(
    12345,
    "Arjan",
    "Sesame street 104",
    "1234",
    "Amsterdam",
    "hi@arjancodes.come"
)

def main():

    vehicle_type = read_vehicle_type(list(VEHICLES.keys()))

    days = read_rent_days()

    additional_km = read_kms_to_drive()

    # setup the rental contract
    rental = RentalContract(
        VEHICLES[vehicle_type],
        customer,
        ContractStatus.ORDERED,
        datetime.now(),
        days,
        max(additional_km - FREE_KMS, 0),
    )

    # log the rental information
    print(rental)

    # calculate the total price
    print(f"Total price: ${rental.total_price/100:.2f}")


if __name__ == "__main__":
    main()
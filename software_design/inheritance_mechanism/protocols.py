import math
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

# Alternative to using ABC - abstract class is to use Protocols
# The Vehicle(Protocol) class has a reserve() method, so...
# the Car and Truck classes, dynamically, are expected to have that method
# whene the reserve_now(vehicle: Vehicle) function is called because it takes a Vehicle Protocol class as input.

# There are no inheritance relationships with Protocols
# There's also NO reason to have a single Protocl class (Vehicle), we can break up the methods into their own classes
# By splitting Vechicle class into Rentable & LicenseHolder Protocols, and isolating reserve and renew_license to separate classes
# instances of these classes no longer _have_ to have both functions
# e.g., note can comment out renew_license() in Car class. 


class Rentable(Protocol):
    def reserve(self, start_date: datetime, days: int):
        ...


class LicenseHolder(Protocol):
    def renew_license(self, new_license_date: datetime):
        ...


@dataclass
class Car:
    model: str
    reserved: bool = False

    def reserve(self, start_date: datetime, days: int):
        self.reserved = True
        print(f"Reserving car {self.model} for {days} days at date {start_date}.")

    # def renew_license(self, new_license_date: datetime):
    #     print(f"Renewing license of car {self.model} to {new_license_date}.")


@dataclass
class Truck:
    model: str
    reserved: bool = False
    reserved_trailer: bool = False

    def reserve(self, start_date: datetime, days: int):
        months = math.ceil(days / 30)
        self.reserved = True
        self.reserved_trailer = True
        print(
            f"Reserving truck {self.model} for {months} month(s) at date {start_date}, including a trailer."
        )

    def renew_license(self, new_license_date: datetime):
        print(f"Renewing license of track {self.model} to {new_license_date}.")


def reserve_now(vehicle: Rentable):
    vehicle.reserve(datetime.now(), 40)


def renew_license_now(license_holder: LicenseHolder):
    license_holder.renew_license(datetime.now())


def main():
    car = Car("Ford")
    truck = Truck("DAF")
    reserve_now(car)
    reserve_now(truck)
    renew_license_now(truck)


if __name__ == "__main__":
    main()

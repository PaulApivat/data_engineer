"""
main() variable has very low cohesion; it's doing too many things (setting price per km/day for each vehicle type);
    then making sure first 100 km is free; then computing final rental price.
1st Solution: introduce Vehical dataclass and dict data structure to capture combination of price per km/day for each vehicle type.
2nd Solution: split behaviors in main() function into their own function
    - separate read_vehicle() function as separate function; set vehicle_type variable in main() to read_vehicle_type() function.
    ** Have read_vehicle() return instance of Vehicle class so main() function is even cleaner
    - separate read_rent_days() function as separate function
    - separate read_kms_to_drive() function as separate function
    - separate compute_rental_cast() function as separate function 
- reference VEHICLE_DATA, store it in vehicle variable in main() function for readability

Summary: Use dataclass and dictionary data structure to improve cohesion of main() function
"""
from dataclasses import dataclass


@dataclass
class Vehicle:
    price_per_day: int
    price_per_km: int


VEHICLE_DATA = {
    "vw": Vehicle(price_per_km=30, price_per_day=6000),
    "bmw": Vehicle(price_per_km=35, price_per_day=8500),
    "ford": Vehicle(price_per_km=25, price_per_day=12000),
}


def read_vehicle() -> Vehicle:
    vehicle_type = ""
    while vehicle_type not in VEHICLE_DATA:
        vehicle_type = input(
            "What type of vehicle would you like to rent (choose vw, bmw, or ford)? "
        )
    return VEHICLE_DATA[vehicle_type]


def read_rent_days() -> int:
    days = 0
    while days < 1:
        days_str = input(
            "How many days would you like to rent the vehicle? (enter a positive number) "
        )
        try:
            days = int(days_str)
        except ValueError:
            print("Invalid input. Please enter a number.")
    return days


def read_kms_to_drive() -> int:
    km = 0
    while km < 1:
        km_str = input(
            "How many kilometers would you like to drive (enter a positive number)? "
        )
        try:
            km = int(km_str)
        except ValueError:
            print("Invalid input. Please enter a number.")
    return km


def compute_rental_cost(vehicle: Vehicle, days: int, km: int) -> int:
    # subtract the base number of kms
    paid_km = max(km - 100, 0)
    return int(vehicle.price_per_day * days + vehicle.price_per_km * paid_km)


def main():
    print("Vehicle Rental before")

    vehicle = read_vehicle()
    rent_days = read_rent_days()
    km = read_kms_to_drive()

    rental_price = compute_rental_cost(vehicle, rent_days, km)

    # print the result
    print(f"The total price of the rental is ${(rental_price / 100):.2f}")


if __name__ == "__main__":
    main()

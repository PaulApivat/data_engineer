from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Customer:
    name: str
    # address: str
    street: str
    postal_code: str
    city: str
    email: str


@dataclass
class Phone:
    brand: str
    model: str
    price: int
    # serial_number: str
    serial: str


@dataclass
class Plan:
    customer: Customer
    phone: Phone
    start_date: datetime
    duration_months: int
    price: int
    phone_included: bool = False

    # def start_date(self, date: datetime):
    #    print(f"Start date is {date}.")

    # def total_month(self, total: int):
    #    total = self.start_date - self.current_date
    #    return total

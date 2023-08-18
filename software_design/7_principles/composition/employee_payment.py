"""
Very advanced Employee management system.
First Attempt: Using Inheritance. 
    - create 3 subclasses: SalariedEmployeeWithCommission(SalariedEmployee), HourlyEmployeeWithCommission(HourlyEmployee), class FreelancerWithCommission(Freelancer)
    - not really a solution, even more code duplication
    - favor code re-use w/ Abstract Base Class or Protocols  
Second Attempt: Using Composition.
    - create class DealBasedCommission, not a sub-class, only responsible for commission and contracts_landed
    - code reuse - add commission attribute to 3 classes: HourlyEmployee, SalariedEmployee and Freelancer (commission: Optional[DealBasedComission] = None)
    - instead of inheritance, we have objects that know about and are connected to each other via instance variables or pass them as parameters (commission: Optional[DealBasedComission] = None)
Third: A More Generic Solution w Abstraction.
    - Use data structures and Protocols to create a more generic version of what we have.
    - Use Protocol: create class PaymentSource(Protocol)
    - create classes based on payment type (HourlyContract, SalariedContract)
    - Turn different employee types into generic class with payment attribute (payment_source: list[PaymentSource])
        - compute_pay function in Employee class is more generic; sum(source.compute_pay() for source in self.payment_sources)
        - all payment_sources, or anything with a compute_pay() function is part of the PaymentSource Protocol. 
note: could also use Abstract Base Class as alternative to Protocol
"""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class PaymentSource(Protocol):
    def compute_pay(self) -> int:
        ...


@dataclass
class DealBasedCommission:
    commission: int = 10000
    contracts_landed: float = 0

    def compute_pay(self) -> int:
        return int(self.commission * self.contracts_landed)


@dataclass
class HourlyContract:
    hourly_rate: int
    hours_worked: float
    employer_cost: int = 100000

    def compute_pay(self):
        return int(self.hourly_rate * self.hours_worked + self.employer_cost)


@dataclass
class SalariedContract:
    monthly_salary: int
    percentage: float = 1

    def compute_pay(self):
        return int(self.monthly_salary * self.percentage)


@dataclass
class Employee:
    name: str
    id: int
    payment_sources: list[PaymentSource] = field(default_factory=list)

    # convenience function for better encapsulation
    def add_payment_source(self, payment_source: PaymentSource):
        self.payment_sources.append(payment_source)

    def compute_pay(self) -> int:
        return sum(source.compute_pay() for source in self.payment_sources)


def main() -> None:
    henry = Employee(name="Henry", id=12346)
    henry.add_payment_source(HourlyContract(hourly_rate=5000, hours_worked=100))
    print(f"{henry.name} earned ${(henry.compute_pay() / 100):.2f}.")

    sarah = Employee(name="Sarah", id=47832)
    sarah.add_payment_source(SalariedContract(monthly_salary=500000))
    sarah.add_payment_source(DealBasedCommission(contracts_landed=10))
    print(f"{sarah.name} earned ${(sarah.compute_pay() / 100):.2f}.")


if __name__ == "__main__":
    main()

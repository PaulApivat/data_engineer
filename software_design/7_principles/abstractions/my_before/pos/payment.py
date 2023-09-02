# from pos.authorization import authorize_google, authorize_robot, authorize_sms
from pos.data import PaymentStatus

# from pos.order import Order
from typing import Callable, Protocol
from dataclasses import dataclass

""" First Abstraction: 
- remove dependency between specific authorization functions and payment processor 
- use type definition to provide this separation 

Solution:
- instead of having authorizer_type as a string, pass the authorizer function - functional approach to solving problem 
- OOP solution is to use "strategy" pattern 
     use type hint AuthorizeFunction as Callable, change authorize parameter to be AuthorizeFunction, remove dependency w pos.authorization 
- Result: PaymentProcessor is no longer responsible for determining what the authorize function is, but passing responsibility to main.py

Second Abstraction: Abstracting the Order Class
- remove Payment Processor dependency on Order class by introducing a Protocol class Payable
- the Payable(Protocol) will have two properties total_price and status, so PaymentProcessor can reference Payable instead of Order
- however, another challenge: order.status requires accessing attribute of Order instance, which we want to avoid
    - solution: define set_status() method in Order class
    - solution: introduce set_status() method in Payable(Protocol)

- Result: We've abstracted away dependcencies on the Order class and no longer requiring knowledge of how authorization is implemented. 
    - instead of dependency hard-coded as string, we're doing dependency injection 
    - The PaymentProcessor is using the AuthorizeFunction which is a Callable 
    - this means any of the 3 authorization.py functions can be used when calling in main()

Third Abstraction: Abstracting the PaymentProcessor 
    - currently, if wanted to add new payment methods (bank_transfer, bitcoin etc) we need to add another method and extend the PaymentProcessor class 
    - currently we have Authorization variety (google, sms) and Payment variety (credit, debit, paypal) that are independent of each other 
    - The Bridge Pattern addresses this specific case of independent variation that rely on each other
    - Authorization & Payment being independent of each other 

Solution:
- create new PaymentProcessor Protocol class w pay() method
    - Bridges authorization and payment method
- create a different class for each Payment type (can even be in different files )

- CreditPaymenntProcessor requires a security_code, since it's a @dataclass, we can set that attribute upon initialization

- AuthorizationFunction is a callable, but only in the main() are things patched together, when importing the different
authorization.py functions; 
"""

AuthorizeFunction = Callable[[], bool]


class Payable(Protocol):
    @property
    def total_price(self) -> int:
        ...

    def set_status(self, status: PaymentStatus):
        ...


class PaymentProcessor(Protocol):
    def pay(self, payable: Payable, authorize: AuthorizeFunction):
        ...


class DebitPaymentProcessor:
    def pay(self, payable: Payable, authorize: AuthorizeFunction):
        if not authorize():
            raise Exception("Not authorized")
        print(
            f"Processing debit payment for amount: ${(payable.total_price / 100):.2f}."
        )
        payable.set_status(PaymentStatus.PAID)


@dataclass
class CreditPaymentProcessor:
    security_code: str

    def pay(self, payable: Payable, authorize: AuthorizeFunction) -> None:
        if not authorize():
            raise Exception("Not authorized")
        print(
            f"Processing credit payment for amount: ${(payable.total_price / 100):.2f}."
        )
        print(f"Verifying security code: {self.security_code}")
        payable.set_status(PaymentStatus.PAID)


@dataclass
class PayPalPaymentProcessor:
    email_address: str

    def pay(self, payable: Payable, authorize: AuthorizeFunction) -> None:
        if not authorize():
            raise Exception("Not authorized")
        print(
            f"Processing PayPal payment for amount: ${(payable.total_price / 100):.2f}."
        )
        print(f"Using email address: {self.email_address}")
        payable.set_status(PaymentStatus.PAID)

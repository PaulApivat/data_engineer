# Functions should do one thing
"""
- Functions should be small
- Function intendation level should be 1-2
    - One level of Abstraction per function 
    - e.g. Mixing level of abstraction (confusing): getHtml()...append("\n")
- Reading Code from Top to Bottom: The Stepdown Rule
- Functions should do one thing
"""

from typing import List, Iterator

class Client:
    def __init__(self, active: bool, name: str):
        self.active = active
        self.name = name


def check_client_status(client: Client) -> None:
    status = "is active" if client.active else "is not active"
    print(f"{client.name} {status}.")
    

def get_active_clients(clients: List[Client]) -> Iterator[str]:
    """Yield name of active clients."""
    return (client.name for client in clients if client.active)


def email_clients(clients: List[Client]) -> None:
    """Send an email to a given list of clients.
    """
    for client in clients:
        check_client_status(client)

# initializing instances of Client class:
if __name__ == "__main__":
    cillian = Client(True, "Cillian")
    matt = Client(False, "Matt")
    emily = Client(True, "Emily")
    oppenheimer_cast = [cillian, matt, emily]
    email_clients(oppenheimer_cast)
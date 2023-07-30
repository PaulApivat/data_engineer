from typing import Generator, Iterator 

class Client:
    def __init__(self, active: bool, name: str):
        self.active = active
        self.name = name


def email(client: Client) -> None:
    status = "is active" if client.active else "is not active"
    print(f"{client.name} {status}.")

def active_clients(clients: Iterator[Client]) -> Generator[Client, None, None]:
    """Only active clients"""
    return (client for client in clients if client.active)


def email_clients(clients: Iterator[Client]) -> None:
    """Send an email to a given list of clients.
    """
    for client in active_clients(clients):
        email(client)

if __name__ == "__main__":
    cillian = Client(True, "Cillian")
    matt = Client(False, "Matt")
    emily = Client(True, "Emily")
    oppenheimer_cast = [cillian, matt, emily]
    email_clients(oppenheimer_cast)
# Functions should do one thing

# To Do: Add Generators
# Description: A client class can be used with various functions. Each function does one thing.


from typing import List



class Client:
    def __init__(self, active: bool, name: str):
        self.active = active
        self.name = name

# initializing instances of Client class:
cillian = Client(True, "Cillian")
matt = Client(False, "Matt")
emily = Client(True, "Emily")
oppenheimer_cast = [cillian, matt, emily]


def email(client: Client) -> None:
    if client.active:
        print(f"{client.name} is active.")
    else:
        print(f"{client.name} not active.")
    

def get_active_clients(clients: List[Client]) -> List[Client]:
    """Yield active clients 
    Turn get_active_clients() into a generator function by using yield
    """
    
    print(f"The following are active")
    for client in clients:
        if client.active:
            yield client.name


def email_clients(clients: List[Client]) -> None:
    """Send an email to a given list of clients.
    """
    for client in clients:
        email(client)


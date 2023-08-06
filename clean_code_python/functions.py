# Functions should do one thing
"""
- Functions should be small
- Function intendation level should be 1-2
    - One level of Abstraction per function 
    - e.g. Mixing level of abstraction (confusing): getHtml()...append("\n")
- Reading Code from Top to Bottom: The Stepdown Rule
- Functions should do one thing
- One Level of Abstraction per Function
- Reading Code from Top to Bottom: The Stepdown Rule
- Switch Statements
- Use descriptive names
- Function Arguments
- Common Monadic Forms
- Flag Arguments
    - Dyadic Functions
    - Triads
- Argument Objects, Argument Lists
- Verbs and Keywords

- Have No Side Effects
    - Output Arguments
    - Command Query Separation
- Prefer Exceptions to Returning Error Codes 
- Extract Try/Catch Blocks
- Error Handling is One Thing
- DRY: Don't Repeat Yourself
- Structured Programming
- Conclusion
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
    for client in get_active_clients(clients):
        print(client)
    #for client in clients:
    #    print(client.name)

# initializing instances of Client class:
if __name__ == "__main__":
    cillian = Client(True, "Cillian")
    matt = Client(False, "Matt")
    emily = Client(True, "Emily")
    oppenheimer_cast = [cillian, matt, emily]
    email_clients(oppenheimer_cast)


# ----------------------- One Level of Abstraction per Function & The Stepdown Rule -----------------------
"""
Each function operates at one level of abstraction:

parse_better_js_alternative Function:

It operates at a high level: tokenizing code and then parsing it. 
It doesn't concern itself with the details of how tokenization or parsing works; 
it just calls the functions that handle those tasks.

tokenize Function:

This function works at the level of reading the code and dividing it into tokens. 
It uses regular expressions to identify and classify parts of the code, but it doesn't need to know the specifics of each regex pattern. 
It knows it needs to find matches for given patterns and classify them.


parse Function:

For the given example, the parsing operation is quite basic, simply grouping the tokens. 
The function is more of a placeholder, but it operates at the level of transforming tokens into a more structured form. 
Again, it doesn't get into the details of how tokenization works, it just works with the results of that process.

To truly embrace "The Stepwown Rule", we should ensure that after any given function, 
the next functions defined are those that it directly calls, in the order they are called.
Hence the ordering:

- parse_better_js_alternatives ->
- tokenize ->
- parse

More Descriptive Names:

- parse_better_js_alternative → parse_and_display_math_expression
- tokenize → extract_tokens_from_expression
- parse → group_tokens_into_syntax_tree

"""

import re 
from typing import Tuple, List, Dict, Union 

# Define regex patterns for numbers
REGEXES: Tuple[Dict[str, str]] = (
    {"type": "NUMBER", "pattern": r"\d+"},
    {"type": "OPERATOR", "pattern": r"[+\-*/]"}
)

def parse_and_display_math_expression(code: str) -> None:
    tokens = extract_tokens_from_expression(code)
    syntax_tree = group_tokens_into_syntax_tree(tokens)

    for node in syntax_tree:
        print(node)

def extract_tokens_from_expression(code: str) -> List[Dict[str, Union[str, int]]]:
    tokens: List[Dict[str, Union[str, int]]] = []

    for regex_info in REGEXES:
        for match in re.finditer(regex_info["pattern"], code):
            tokens.append({"type": regex_info["type"], "value": match.group()})

    return tokens

def group_tokens_into_syntax_tree(tokens: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
    # For this example, the parsing will just group numbers and operators 
    syntax_tree: List[Dict[str, Union[str, int]]] = [{"group": tokens}]
    return syntax_tree



code = "3 + 5 - 2"
parse_and_display_math_expression(code)

# ---------------- Don't use flags as function parameters-----------------

"""
The function create_file violates the "functions should do one thing" principle 
because it's making decisions based on the in_temp_directory parameter about where to create the file: 
either in the temporary directory or at the given path. 

Essentially, it's combining two responsibilities:

1. Deciding the directory in which the file should be created.
2. Actually creating the file.

To adhere to the principle, we should separate these two responsibilities into distinct functions.
"""

# This example violates the principle
from tempfile import gettempdir
from pathlib import Path 

def create_file(name: str, in_temp_directory: bool = False) -> Path:
    if in_temp_directory:
        file_path = Path(gettempdir()) / name 
    else:
        file_path = Path(name)

    file_path.touch()
    return file_path

# Example of usage:
new_file = create_file("test.txt", in_temp_directory=True)
print(f"File created at: {new_file}")


"""
To adhere to the principle, we should separate these two responsibilities into distinct functions. 
One function should determine the path, and the other should handle file creation.

Here's a refactor to separate these responsibilities:
"""
from tempfile import gettempdir
from pathlib import Path 


def determine_path(name: str, in_temp_directory: bool = False) -> Path:
    """
    Determine the full path where a file should be created.

    Args:
    - name (str): Name of the file. This can be a relative or absolute path.
    - in_temp_directory (bool, optional): If True, the path is determined within the system's temporary directory.
                                          Otherwise, it's determined based on the provided name.
                                          Defaults to False.

    Returns:
    - Path: The full path where the file should be created.
    """
    return Path(gettempdir()) / name if in_temp_directory else Path(name)

def create_file_at_path(file_path: Path) -> None:
    """
    Create a new file at the specified path.

    Args:
    - file_path (Path): The full path where the file should be created.

    Returns:
    - Path: The full path to the created file.
    """
    file_path.touch()
    return file_path

path_to_create = determine_path("test.txt", in_temp_directory=True)
new_file = create_file_at_path(path_to_create)
print(f"File created at: {new_file}")



# ------------ AVOID Side Effects ----------------------------

"""
The side effect:

1. Before calling the function, fullname is "Ryan McDermott".
2. After calling the function, the fullname variable is changed to ['Ryan', 'McDermott'].

This change in state (from a string to a list) is the side effect of the function.
"""

fullname = "Ryan McDermott"

def split_into_first_and_last_name() -> None:
    global fullname
    fullname = fullname.split()

split_into_first_and_last_name()

print(fullname)


"""
Avoid the side effect by having the function return a new value 
without modifying the external state, which exists outside the function's scope
"""

fullname = "Bill Hader"

def split_into_first_and_last_name(name: str) -> list:
    return name.split()

new_name_format = split_into_first_and_last_name(fullname)

print(fullname)
print(new_name_format)

"""
Another example of avoiding side effects
"""

from typing import List, AnyStr

def split_into_first_and_last_name(name: AnyStr) -> List[AnyStr]:
    return name.split()

fullname = "Conan O'Brien"
name, surname = split_into_first_and_last_name(fullname)

print(fullname)
print(name)
print(surname)


"""
dataclasses help manage state, so also help avoid side-effects
"""
from dataclasses import dataclass
from typing import List

@dataclass
class Person:
    """
    Represents a person with a given name.
    """
    name: str

    @property
    def split_name_into_parts(self) -> List[str]:
        """
        Splits the name of the person into its components (e.g., first name and last name).

        Returns:
            List[str]: A list containing components of the name.
        """
        return self.name.split()

# Example usage
person = Person("Julia Roberts")

print(f"Full Name: {person.name}")
print(f"Name Parts: {person.split_name_into_parts}")
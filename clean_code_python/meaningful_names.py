"""
Clean Code: Meaningful Names (Ch 2)
- Use intention revealing names
- Avoid Disinformation
- Make Meaningful Distinctions
- Use Pronounceable Names
- Use Searchable Names
- Avoid Encodings
- Avoid Mental Mapping (using single letters 'l' so users have to map to the actual concept)
- Class Names: classes and objects should be nouns
- Method Names: methods should be verbs
- Don't be cute
- Pick One Word per Concept
- Don't pun
- Use Solution Domain Names
- Use Problem Domain Names
- Add meaningful context
- Don't add gratuitous context

"""

# Use intention revealing, meaningful and pronounceable names
import datetime 

# bad
ymdstr = datetime.date.today().strftime("%y-%m-%d")

# good
current_date: str = datetime.date.today().strftime("%y-%m-%d")

# Avoid:
# getActiveAccounts() vs getActiveAccounts() vs getActiveAccountInfo()

# Use the same vocabulary for the same type of variable

# bad
def get_user_info():
    pass

def get_client_data():
    pass

def get_customer_record():
    pass 

# good
def get_user_info():
    pass

def get_user_data():
    pass

def get_user_record():
    pass

# Even Better 
# 
# use object oriented feature to package function together as instance attributes or property methods

from typing import Union, Dict 

class Record:
    pass 

class User:
    info: str

    @property
    def data(self) -> Dict[str, str]:
        return {}

    def get_record(self) -> Union[Record, None]:
        return Record()

"""
Even Better example could _still_ be improved with:
- type annotations and constructors
- docstrings
- defining the Record class
- Return Type simplification: Use Optional[Record] instead of Union[Record, None]
- Improve Property Data
"""

from typing import Optional, Dict

class Record:
    # Example attributes; modify as needed
    content: str 

    def __init__(self, content: str):
        """Initialize the Record with content."""
        self.content = content 

    def __repr__(self) -> str:
        return f"Record(content={self.content})"

class User:
    def __init__(self, info: str):
        """Initialize the User with info."""
        self.info = info

    @property
    def data(self) -> Dict[str, str]:
        """Return the user's data as a dictionary.
        For this example, it simply returns the info attribute. Modify as needed."""
        return {'info': self.info}

    def get_record(self) -> Optional[Record]:
        """Return a Record associated with the user.
        In this example, it returns as new Record with the user's info. Modify as needed."""
        return Record(self.info)

# Example usage
user = User("User information here")
print(user.data)
print(user.get_record())


# Use Searchable Names

# bad
import time 

# What is the number 86400 for again?
# time.sleep(86400)

# Declear them in a global namespace for the module
SECONDS_IN_A_DAY = 60 * 60 * 24
# time.sleep(SECONDS_IN_A_DAY)


# Use Explanatory Variables 

# bad
import re 

address = "One Infinite Loop, Cupertino 95014"
city_zip_code_regex = r"^[^,\\]+[,\\\s]+(.+?)\s*(\d{5})?$"

# matches = re.match[city_zip_code_regex, address]
# if matches:
#    print(f"{matches[1]}: {matches[2]}")


# good
import re

address = "One Infinite Loop, Cupertino 95014"
city_zip_code_regex = r"^[^,\\]+[,\\\s]+(?P<city>.+?)\s*(?P<zip_code>\d{5})?$"

matches = re.match(city_zip_code_regex, address)
if matches:
    print(f"{matches['city']}, {matches['zip_code']}")

"""
Use Better Explanatory Variables can still be improved
- use comments
- break down the regex pattern
- add error handling
- function encapsulation 
"""

import re

def extract_city_zip_code(address: str) -> None:
    # Break down regex into understandable parts
    start_pattern = r"^[^,\\]+[,\\\s]+"  # Match start until the first comma or backslash
    city_pattern = r"(?P<city>.+?)\s*"   # Match and name the city part
    zip_code_pattern = r"(?P<zip_code>\d{5})?$" # Match and name the zip code part (5 digits)

    # Combine the patterns
    city_zip_code_regex = start_pattern + city_pattern + zip_code_pattern 

    matches = re.match(city_zip_code_regex, address)

    # Check if the address matches the pattern and print the city and zip code
    if matches:
        print(f"{matches['city']}, {matches['zip_code']}")
    else:
        print("Address format is not recognized.")

# Example Usage
address = "One Infinite Loop, Cupertino 95014"
extract_city_zip_code(address)


# Avoid Mental Mapping

# bad
seq = ("Austin", "New York", "San Francisco")

for item in seq:
    print(item)

# good
locations = ("Austin", "New York", "San Francisco")

for location in locations:
    print(location)

# Don't add unneeded context

# bad
class Car:
    car_make: str
    car_model: str
    car_color: str


# good
class Car:
    make: str
    model: str
    color: str 


# Use Default arguments instead of conditions

# bad
import hashlib

# def create_micro_brewery(name):
#    name = "Hipster Brew Co." if name is None else name
#    slug = hashlib.sha1(name.encode()).hexdigest()
#    print(slug)


def create_micro_brewery(name: str = "Hipster Brew Co."):
    slug = hashlib.sha1(name.encode()).hexdigest()
    print(slug)

create_micro_brewery()
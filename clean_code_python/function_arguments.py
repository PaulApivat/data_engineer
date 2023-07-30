# Function arguments (2 or fewer ideally)
"""
A large amount of parameters is usually the sign that a function is doing too much (has more than one responsibility). 
Try to decompose it into smaller functions having a reduced set of parameters, ideally less than three.
"""

from dataclasses import astuple, dataclass

@dataclass
class MenuConfig:
    """A configuration for the Menu.

    Attributes:
        title: The title of the Menu.
        body: The body of the Menu.
        button_text: The text for the button label.
        cancellable: Can it be cancelled?
    """
    title: str 
    body: str 
    button_text: str 
    cancellable: bool = False 


def create_menu(config: MenuConfig):
    """Creates and displays a menu given a MenuConfig."""
    title, body, button_text, cancellable = astuple(config)
    print(f"{title}\n{body}\n{button_text}\nCancellable: {cancellable}")


if __name__ == "__main__":
    create_menu(
        MenuConfig(
            title="My delicious menu",
            body="A description of various items in the menu",
            button_text="Order now!"
        )
    )

# creating a default menu
menu_config = MenuConfig("Title", "Body", "Button")
create_menu(menu_config)

# changing menu configuration
menu_config.button_text = "New Button Text"
create_menu(menu_config)

# creating a cancellable menu
cancellable_menu_config = MenuConfig("Title", "Body", "Button", True)
create_menu(cancellable_menu_config)




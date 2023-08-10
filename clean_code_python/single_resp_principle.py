# Classes
## Single Responsibility Principle (SRP)

"""Bad Example of SRP: This class does two things (instead of one)

class VersionCommentElement:

    def get_version(self) -> str:
        return metadata.version("pip")

    def render(self) -> None:
        print(f'<!-- Version: {self.get_version()} -->')

VersionCommentElement().render()

"""

from importlib import metadata 

def get_version(pkg_name: str) -> str:
    """Retrieve the version of a given package"""
    return metadata.version(pkg_name)


class VersionCommentElement:
    """An element that renders an HTML comment with the program's version number.
    The class only needs to take care of rendering. The get_version() funcion is called outside the class.
    """
    def __init__(self, version: str):
        self.version = version

    def render(self) -> None:
        print(f'<!-- Version: {self.version} -->')

VersionCommentElement(get_version("pip")).render()
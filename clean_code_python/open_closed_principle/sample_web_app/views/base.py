from abc import ABC, abstractmethod
from models.response import Response 

class View(ABC):
    """An absract view class
    
    Instead of hardcoding the response in the View class, 
    allow subclasses to define the specifics of their responses. 
    This way, the View class sets the general structure and behavior, 
    and subclasses fill in the specifics.
    """

    @abstractmethod
    def get(self, request) -> Response:
        """An abstract method to handle a GET request and return a response"""
        pass 
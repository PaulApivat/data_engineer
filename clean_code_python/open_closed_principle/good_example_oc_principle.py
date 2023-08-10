from dataclasses import dataclass 
from abc import ABC, abstractmethod

@dataclass
class Response:
    """An HTTP response"""
    status: int 
    content_type: str 
    body: str 


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


class PlainTextView(View):

    def get(self, request) -> Response:
        return Response(
            status=200,
            content_type='text/plain',
            body="Welcome to my site"
        )

class TemplateView(View):

    def get(self, request) -> Response:
        with open("index.html") as fd:
            return Response(
                status=200,
                content_type='text/html',
                ody=fd.read()
            )


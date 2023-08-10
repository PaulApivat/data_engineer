from dataclasses import dataclass 

@dataclass
class Response:
    """An HTTP Response"""
    status: int 
    content_type: str 
    body: str 


class View:
    """A simple view that returns plain text responses."""
    def get(self, request) -> Response:
        """Handle a GET request and return a message in the response."""
        return Response(
            status=200,
            content_type='text/plain',
            body='Welcome to my web site.'
        )

class TemplateView(View):
    """A view that returns HTML responses based on a template file."""
    def get(self, request) -> Response:
        """Handle a GET request and return an HTML document in the response."""
        with open("intex.html") as fd:
            return Response(
                status=200,
                content_type="text/html",
                body=fd.read()
            )
from models.request import HttpRequest 
from models.response import Response
from views.plain import PlainTextView 
from views.template import TemplateView 
from router import Router 

def print_response(response: Response):
    """Helper function to display the response."""
    print(f"Status: {response.status}")
    print(f"Content-Type: {response.content_type}")
    print(f"Body: {response.body[:100]}...")  # Only display the first 100 characters for brevity

def main():
    # Create some views
    plain_view = PlainTextView()
    template_view = TemplateView()

    # Create a router and register the views
    router = Router()
    router.register("/plain", plain_view)
    router.register("/template", template_view)

    # Simulate some requests
    plain_request = HttpRequest(method='GET', path='/plain', headers={})
    template_request = HttpRequest(method='GET', path='/template', headers={})
    unknown_request = HttpRequest(method='GET', path='/unknown', headers={})

    # Handle and print responses for simulated requests
    print("Response for /plain:")
    print_response(router.handle_request(plain_request))
    print("\n------------------\n")

    print("Response for /template:")
    print_response(router.handle_request(template_request))
    print("\n------------------\n")

    print("Response for /unknown:")
    print_response(router.handle_request(unknown_request))
    print("\n------------------\n")

if __name__ == "__main__":
    main()
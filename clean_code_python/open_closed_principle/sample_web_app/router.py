from models.response import Response 

class Router:

    def __init__(self):
        self.routes = {}

    def register(self, path: str, view):
        self.routes[path] = view 

    def handle_request(self, request) -> Response:
        if request.path in self.routes:
            return self.routes[request.path].get(request)
        else:
            return Response(400, 'text/plain', 'Not Found')
from models.response import Response 
from views.base import View

class PlainTextView(View):

    def get(self, request) -> Response:
        return Response(
            status=200,
            content_type='text/plain',
            body="Welcome to my site"
        )
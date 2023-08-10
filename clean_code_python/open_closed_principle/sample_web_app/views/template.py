from models.response import Response 
from views.base import View 

class TemplateView(View):

    def get(self, request) -> Response:
        with open("index.html") as fd:
            return Response(
                status=200,
                content_type='text/html',
                body=fd.read()
            )
from django.http import HttpResponse
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView


def index(request):
    return HttpResponse(template_200)


template_200 = """
    <h1 style='text-align:center'>200 OK!</h1>
    <br/> 
    <p style='text-align:center;'>
        Web server <strong>up and running</strong> successfully
    </p>
"""
template_400 = """
    <h1 style='text-align:center'>404!</h1>
    <br/> 
    <p style='text-align:center'>
        This is not the page you're looking for.
    </p>
"""


class NotFoundView(APIView):
    permission_classes = []

    def process_response(self, request):
        import secrets

        data = {
            "status": 404,
            "error": "This route does not exists",
            "message": "You've hit web server perfectly! perhaps you missed the url address",
            "request": {},
        }
        account = request.user
        if account.is_authenticated:
            profile_type, profile = request.user.get_profile()  # type: ignore
            data["request"]["Authenticated"] = True
            data["request"]["User"] = {
                "Account Type": profile_type,  # type: ignore
                "Full Name": account.full_name,  # type: ignore
                "Last Login": (
                    str(account.last_login.__format__("%m/%d/%Y %H:%M:%S"))
                    if account.last_login
                    else None
                ),
            }
        else:
            data["request"]["Authenticated"] = False

        data["request"]["Intent"] = "WEB SERVER"
        data["request"]["Origin"] = request.headers.get("origin") or "Unknown"
        data["request"]["Hash-Key"] = secrets.token_hex(12)
        data["request"]["Client Agent"] = request.headers.get("User-Agent")

        return Response(data, status=404)

    def get(self, request, *args, **kwargs):
        return self.process_response(request)

    def post(self, request, *args, **kwargs):
        return self.process_response(request)

    def put(self, request, *args, **kwargs):
        return self.process_response(request)

    def delete(self, request, *args, **kwargs):
        return self.process_response(request)

    def patch(self, request, *args, **kwargs):
        return self.process_response(request)

    def options(self, request, *args, **kwargs):
        return self.process_response(request)


class APINotFoundView(APIView):
    permission_classes = []

    def process_response(self, request):
        import secrets

        data = {
            "status": 404,
            "error": "This route does not exists",
            "message": "You've hit our api server successfully! perhaps you missed the url address",
            "request": {},
        }
        account = request.user
        if account.is_authenticated:
            profile_type, profile = request.user.get_profile()  # type: ignore
            data["request"]["Authenticated"] = True
            data["request"]["User"] = {
                "Account Type": profile_type,  # type: ignore
                "Full Name": account.full_name,  # type: ignore
                "Last Login": str(account.last_login.__format__("%m/%d/%Y %H:%M:%S")),  # type: ignore
            }
        else:
            data["request"]["Authenticated"] = False

        data["request"]["Intent"] = "API SERVER"
        data["request"]["Origin"] = request.headers.get("origin") or "Unknown"
        data["request"]["Hash-Key"] = secrets.token_hex(12)
        data["request"]["Client Agent"] = request.headers.get("User-Agent")

        return Response(data, status=404)

    def get(self, request, *args, **kwargs):
        return self.process_response(request)

    def post(self, request, *args, **kwargs):
        return self.process_response(request)

    def put(self, request, *args, **kwargs):
        return self.process_response(request)

    def delete(self, request, *args, **kwargs):
        return self.process_response(request)

    def patch(self, request, *args, **kwargs):
        return self.process_response(request)

    def options(self, request, *args, **kwargs):
        return self.process_response(request)

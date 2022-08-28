from rest_framework import status as res_status


class ForceJSON400Middleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == res_status.HTTP_400_BAD_REQUEST:
            response["Content-Type"] = "application/json"

        return response

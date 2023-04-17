from django.shortcuts import redirect

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            if request.user.is_authenticated:
                return redirect('Home')
            else:
                return redirect('login')

        return response

from django.shortcuts import redirect
from django.urls import reverse
from .models import CustomUser

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow users to reach the login page
        if request.path == reverse('admin:login'):
            return self.get_response(request)
        if request.path.startswith(reverse('admin:index')) and not request.user.is_authenticated:
            return redirect('admin:login')  # Redirect non-authenticated users to the admin login page
        if request.user.is_authenticated and not request.user.is_superuser and request.user.role != CustomUser.ADMIN:
            return redirect('/')  # Redirect non-admin users to the homepage
        return self.get_response(request)

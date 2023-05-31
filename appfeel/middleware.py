from django.shortcuts import redirect
from django.urls import reverse
from .models import CustomUser

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')) and not request.user.is_superuser and request.user.role != CustomUser.ADMIN:
            return redirect('/')  # Cambia 'home' a la URL deseada para redireccionar a los usuarios no administradores
        return self.get_response(request)

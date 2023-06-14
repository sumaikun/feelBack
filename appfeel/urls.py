from django.urls import include, path
from . import views
from rest_framework import routers
from .views import LoginView, UserViewSet, validate_token

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('generate_text/', views.generate_text, name='generate_text'),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/validate-token/<str:token>/', validate_token, name='validate_token')
]

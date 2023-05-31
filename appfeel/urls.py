from django.urls import include, path
from . import views
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('generate_text/', views.generate_text, name='generate_text'),
    path('api/', include(router.urls))
]

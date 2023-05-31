import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feel.settings')
django.setup()

from django.contrib.auth.models import Permission, ContentType
from appfeel.models import CustomUser

def create_can_create_doctor_permission():
    content_type = ContentType.objects.get_for_model(CustomUser)
    permission, created = Permission.objects.get_or_create(
        codename='can_create_doctor',
        name='Can create doctor',
        content_type=content_type
    )
    print('Permiso "Can create doctor" creado con éxito.')

create_can_create_doctor_permission()

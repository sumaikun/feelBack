from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_doctor(self, username, email, password=None):
        user = self.model(username=username, email=email,
                          role=CustomUser.DOCTOR)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractUser):
    ADMIN = 'ADMIN'
    DOCTOR = 'DOCTOR'
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (DOCTOR, 'Doctor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


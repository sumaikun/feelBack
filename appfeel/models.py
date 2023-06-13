from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_doctor(self, username, email, password=None):
        user = self.model(username=username, email=email,
                          role=CustomUser.DOCTOR)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password):
      """
      Create and return a `User` with superuser powers.

      Superuser powers means that this use is an admin that can do anything
      they want.
      """
      if password is None:
          raise TypeError('Superusers must have a password.')

      user = self.model(username=username, email=email,
                          role=CustomUser.ADMIN)
      user.set_password(password)  
      user.is_superuser = True
      user.is_staff = True
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

    def __str__(self):
        return self.username
    
class Therapies(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    acronyms = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Therapy'  # Singular name
        verbose_name_plural = 'Therapies'  # Plural name

    

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile', unique=True)
    speciality = models.CharField(max_length=100)
    therapies = models.ManyToManyField(Therapies, related_name='doctors', blank=True)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_doctor', unique=True)
    anonymous_name = models.CharField(max_length=100, blank=True, null=True)
    anonymous_email = models.EmailField(blank=True, null=True)
    anonymous_phone = models.CharField(max_length=20, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name


class Conversation(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    anonymous_name = models.CharField(max_length=100, blank=True, null=True)
    anonymous_email = models.EmailField(blank=True, null=True)
    anonymous_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.content[:50]

    class Meta:
        ordering = ['created_at']
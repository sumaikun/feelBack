from django import forms
from .models import CustomUser, DoctorProfile

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['user', 'speciality', 'therapies', 'image']  # List your fields here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(role=CustomUser.DOCTOR)

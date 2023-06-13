from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from .forms import DoctorProfileForm
from .models import CustomUser, Therapies, DoctorProfile
from django.http import HttpResponseRedirect


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [DoctorProfileInline]
    list_display = ('username', 'email', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'role')}),
        ('Permissions', {'fields': ('is_active',
                                    'is_staff', 'is_superuser', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'user_permissions'),
        }),
    )
    filter_horizontal = ('user_permissions',)

    def save_model(self, request, obj, form, change):
        # Check if the logged-in user is a doctor, if so prevent them from saving
        if request.user.role == CustomUser.DOCTOR:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "You don't have permission to save users")
            return  # Exit the function to prevent saving
            
        # Check if the logged-in user is an admin and trying to save a superuser, if so prevent them from saving
        elif request.user.role == CustomUser.ADMIN and obj.is_superuser:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "You don't have this permission")
            return  # Exit the function to prevent saving

        # Call the superclass's save_model method to handle the actual saving
        super().save_model(request, obj, form, change)

        # If the user being saved is a doctor and this is a new record, create a related DoctorProfile
        if obj.role == CustomUser.DOCTOR and not change:
            doctor_profile = DoctorProfile(user=obj)
            doctor_profile.save()


    def get_readonly_fields(self, request, obj=None):
        if obj and obj.role == CustomUser.ADMIN and not request.user.is_superuser:
            return ('username', 'email', 'role', 'is_superuser', 'is_staff', 'is_active')
        return ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_authenticated and not request.user.is_superuser:
            #qs = qs.exclude(role=CustomUser.ADMIN)
            qs = qs.exclude(Q(is_superuser=True) | (Q(role=CustomUser.ADMIN) & ~Q(id=request.user.id)))
        return qs

    def get_inline_instances(self, request, obj=None):
        if obj and obj.role == CustomUser.DOCTOR:
            return [DoctorProfileInline(self.model, self.admin_site)]
        return []
    
    def get_fieldsets(self, request, obj=None):
        # Get default fieldsets
        fieldsets = super().get_fieldsets(request, obj)
        print(fieldsets)
        # If the user is not a superuser, remove the 'Superuser status' field
        if not request.user.is_superuser:
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                ('Personal Info', {'fields': ('email', 'role')}),
                ('Permissions', {'fields': ('is_active',
                                            'is_staff', 'user_permissions')}),
            )
        if request.user.role == CustomUser.DOCTOR:
              fieldsets = (
                (None, {'fields': ('username', 'password')}),
                ('Personal Info', {'fields': ('email', 'role')}),
            )
        return fieldsets


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Therapies)
class TherapiesAdmin(admin.ModelAdmin):
    pass

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    form = DoctorProfileForm

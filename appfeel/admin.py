from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
        if obj.role == CustomUser.DOCTOR:
            if obj.role == CustomUser.ADMIN and not request.user.has_perm('appfeel.can_create_doctor'):
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        if obj.role == CustomUser.ADMIN:
            if str(request.user.id) == str(obj.id):
                return HttpResponseRedirect('/')
            else:
                obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if request.user.is_authenticated:
            if obj and obj.role == CustomUser.ADMIN and not request.user.is_superuser:
                self.readonly_fields = ('username', 'email', 'role', 'is_superuser', 'is_staff', 'is_active')
            else:
                self.readonly_fields = ()
        return super().change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                qs = qs.exclude(role=CustomUser.ADMIN)
        return qs

    def get_inline_instances(self, request, obj=None):
        if obj and obj.role == CustomUser.DOCTOR:
            return [DoctorProfileInline(self.model, self.admin_site)]
        return []


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Therapies)
class TherapiesAdmin(admin.ModelAdmin):
    pass

@admin.register(DoctorProfile)
class TherapiesAdmin(admin.ModelAdmin):
    pass

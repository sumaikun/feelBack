from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.http import HttpResponseRedirect


class CustomUserAdmin(UserAdmin):
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
        if obj and obj.role == CustomUser.ADMIN and not request.user.is_superuser:
            self.readonly_fields = ('username', 'email', 'role', 'is_superuser', 'is_staff', 'is_active')
        else:
            self.readonly_fields = ()
        return super().change_view(request, object_id, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and obj.role == CustomUser.ADMIN and not request.user.is_superuser:
            self.fields = ('password',)
            self.readonly_fields = (
                'username', 'email', 'role', 'is_superuser', 'is_staff', 'is_active')
        else:
            self.fields = '__all__'
            self.readonly_fields = ()
        return super().change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(role=CustomUser.ADMIN)
        return qs


admin.site.register(CustomUser, CustomUserAdmin)

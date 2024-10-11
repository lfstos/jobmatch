from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.usuario.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_company')
    list_filter = ('is_staff', 'is_active', 'is_company')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_company')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class AdminUser(UserAdmin):
    UserAdmin.fieldsets[2][1]['fields'] = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'avatar', 'phone', 'web', 'bio', 'status', 'IP')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'IP')

admin.site.register(User, AdminUser)

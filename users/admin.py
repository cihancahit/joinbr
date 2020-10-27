from .models import UserProfileModel, UserRSS, User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'fullname', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'fullname', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class UserRssAdmin(admin.ModelAdmin):
    list_display = ('title',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(UserProfileModel, UserProfileAdmin)
admin.site.register(UserRSS, UserRssAdmin)
admin.site.register(User, UserAdmin)

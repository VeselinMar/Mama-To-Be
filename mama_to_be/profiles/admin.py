from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from mama_to_be.profiles.models import AppUser, Profile


# Register your models here.

@admin.register(AppUser)
class AppUserAdmin(UserAdmin):

    # Fields to display in admin list view
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display in the admin detail/edit view
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    # Fields to display in the admin list view
    list_display = ('user', 'username', 'profile_picture',)
    search_fields = ('user__email', 'username')
    list_filter = ('user__is_active',)

    # Fields to display in the admin detail/edit view
    fieldsets = (
        (None, {'fields': ('user', 'username', 'profile_picture',)}),
    )

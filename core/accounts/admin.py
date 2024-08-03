from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "is_superuser", "is_active")
    list_filter = ("username", "email","is_superuser", "is_active")
    search_fields = ("username","email")
    ordering = ("username",)
    fieldsets = (
        ("Authentication", {"fields": ("username", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                )
            },
        ),("Group Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },),("Important dates",
            {
                "fields": (
                    "last_login",
                )
            },),
    )
    add_fieldsets = (
        (
            "Create",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        ("User Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            }),
    )

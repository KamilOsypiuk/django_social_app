from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "date_of_birth", "phone_number"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "date_of_birth",
                    "phone_number",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "date_of_birth", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)

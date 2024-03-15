from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "password",
                    "name",
                    "email",
                    "tel",
                    "birthday",
                    "marketing_agree_yn",
                ),
            },
        ),
    )

    list_display = ("username", "email", "name")

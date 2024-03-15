from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "address_name",
        "address",
        "address_detail",
        "zip_code",
    ]

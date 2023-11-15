from django.contrib import admin
from .models import (
    Contact,
    PhoneNumber,
)


class PhoneNumberInLine(admin.TabularInline):
    model = PhoneNumber
    extra = 0


class ContactAdmin(admin.ModelAdmin):
    inlines = [
        PhoneNumberInLine,
    ]
    list_display = (
        "last_name",
        "first_name",
        "email",
    )


admin.site.register(Contact, ContactAdmin)
admin.site.register(PhoneNumber)

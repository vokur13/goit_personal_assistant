from django.contrib import admin
from .models import Contact, PhoneNumber


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "email",
    )


# class PhoneNumberAdmin(admin.ModelAdmin):
#     list_display = (
#         "number",
#         "contact",
#     )


admin.site.register(Contact, ContactAdmin)
# admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(PhoneNumber)

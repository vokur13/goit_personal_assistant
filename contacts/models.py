from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
import re

from phonenumber_field.modelfields import PhoneNumberField

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


class Contact(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()  # Reduces junk to ""
        if self.email != "":  # If it's not blank
            if not re.match(regex, self.email):  # If it's not an email address
                raise ValidationError("%s is not an email address, dummy!" % self.email)
        if self.email == "":
            self.email = None
        super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        return self.last_name + ", " + self.first_name

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self.pk})


class PhoneNumber(models.Model):
    phone_number = PhoneNumberField(blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        # return f"{self.contact}: {str(self.phone_number)}"
        return f"{str(self.phone_number)}"

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self})

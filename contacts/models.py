from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
import re
from birthday import BirthdayField, BirthdayManager


regex_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
regex_phone_number = r"[+]\d{9,12}$"


class Contact(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    dob = BirthdayField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    objects = BirthdayManager()

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()  # Reduces junk to ""
        if self.email != "":  # If it's not blank
            if not re.match(regex_email, self.email):  # If it's not an email address
                raise ValidationError("%s це не адреса електронної пошти!" % self.email)
        if self.email == "":
            self.email = None
        super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        return self.last_name + ", " + self.first_name

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self.pk})


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=24, blank=True, null=True, unique=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.phone_number = self.phone_number.lower().strip()  # Reduces junk to ""
        if self.phone_number != "":  # If it's not blank
            if not re.match(
                regex_phone_number, self.phone_number
            ):  # If it's not a phone number
                raise ValidationError(
                    "%s недійсний номер телефону!" % self.phone_number
                )
        if self.phone_number == "":
            self.phone_number = None
        super(PhoneNumber, self).save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.phone_number)}"

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self})

import os
import random
import re
import sys

import django
import transliterate
from faker import Faker
from phonenumber_field.phonenumber import PhoneNumber as ph_nu

sys.path.append(
    "/Users/vokur/PycharmProjects/djangoProject/personal_assistant/django_project/django_project"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()


from accounts.models import CustomUser
from contacts.models import Contact, PhoneNumber

fake = Faker("uk_UA")

NUMBER_OF_CONTACTS = 200


def transliterate_ukrainian_to_english(text):
    text = text.replace("'", "_")
    result = transliterate.translit(text.lower(), "uk", reversed=True)
    return result


def person_email(first_name, last_name):
    fake_email = f"{transliterate_ukrainian_to_english(first_name)}.{transliterate_ukrainian_to_english(last_name)}@{fake.free_email_domain()}"

    return fake_email


def sanitize_email(email):
    # Replace special characters with underscores
    sanitized_email = re.sub(r"[^a-zA-Z0-9.@_]+", "_", email)

    # Ensure the email address starts and ends with alphanumeric characters
    sanitized_email = re.sub(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$", "", sanitized_email)

    return sanitized_email


def create_contact():
    Contact.objects.all().delete()
    users = CustomUser.objects.all()
    for _ in range(NUMBER_OF_CONTACTS):
        first_name = fake.first_name()
        last_name = fake.last_name()
        address = fake.street_address()
        city = fake.city()
        full_address = address + ", " + city
        email = person_email(first_name, last_name)
        sanitized_email = sanitize_email(email)
        dob = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=65)
        notes = fake.text(max_nb_chars=100)
        row = Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=full_address,
            email=sanitized_email,
            dob=dob,
            notes=notes,
            owner=random.choice(users),
        )
        row.save()


def create_phone_number():
    PhoneNumber.objects.all().delete()
    contacts = Contact.objects.all()
    for contact in contacts:
        number = f"+380{fake.msisdn()[4:]}"
        number_reg = ph_nu.from_string(number, region="UA")
        row = PhoneNumber.objects.create(
            phone_number=number_reg.as_e164, contact=contact
        )
        row.save()


if __name__ == "__main__":
    create_contact()
    create_phone_number()

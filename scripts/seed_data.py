import asyncio
import os
import sys
import django

from faker import Faker
from transliterate import translit
from phonenumber_field.phonenumber import PhoneNumber as PhNu

from django_project.settings import env

sys.path.append(
    "/Users/vokur/PycharmProjects/djangoProject/personal_assistant/django_project/django_project"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


from accounts.models import CustomUser
from contacts.models import Contact, PhoneNumber

fake = Faker("uk_UA")
APP_USER_NAME = env.str("APP_USER_NAME")
NUMBER_OF_CONTACTS = int(env.str("NUMBER_OF_CONTACTS"))


async def translit_person_name(name):
    name_translit = ""
    for char in translit(name.lower(), "uk", reversed=True):
        if "'" in char:
            # name_translit += "_"
            continue
        name_translit += char
    return name_translit


async def person_email(first_n, last_n):
    first_name_translit = await translit_person_name(first_n)
    last_name_translit = await translit_person_name(last_n)
    return f"{first_name_translit}.{last_name_translit}@{fake.free_email_domain()}"


async def create_contact():
    Contact.objects.all().delete()
    users = CustomUser.objects.all()
    for _ in range(NUMBER_OF_CONTACTS):
        given_name = fake.first_name()
        surname_name = fake.last_name()
        address = fake.street_address()
        city = fake.city()
        full_address = address + ", " + city
        email = await person_email(given_name, surname_name)
        dob = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=65)
        notes = fake.text(max_nb_chars=100)
        for user in users:
            if user.username == APP_USER_NAME:
                row = Contact.objects.create(
                    first_name=given_name,
                    last_name=surname_name,
                    address=full_address,
                    email=email,
                    dob=dob,
                    notes=notes,
                    owner=user,
                )
                row.save()


async def create_phone_number():
    PhoneNumber.objects.all().delete()
    contacts = Contact.objects.all()
    for contact in contacts:
        number = f"+380{fake.msisdn()[4:]}"
        number_reg = PhNu.from_string(number, region="UA")
        row = PhoneNumber.objects.create(
            phone_number=number_reg.as_e164, contact=contact
        )
        row.save()


if __name__ == "__main__":
    asyncio.run(create_contact())
    asyncio.run(create_phone_number())

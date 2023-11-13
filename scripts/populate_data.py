# import json
import os
import sys
from datetime import datetime

from faker import Faker
from transliterate import translit

import django

from contacts.models import Contact

from django.contrib.auth import get_user_model

from django_project.settings import AUTH_USER_MODEL

# from django_project import settings

# os.environ["DJANGO_SETTINGS_MODULE"] = "django_project.settings"
# sys.path.append(
#     "/Users/vokur/PycharmProjects/djangoProject/personal_assistant/django_project/django_project"
# )
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

fake = Faker("uk_UA")


def create_contacts():
    # Contact.objects.all().delete()

    for _ in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        first_name_translit = translit(first_name.lower(), "uk", reversed=True)
        last_name_translit = translit(last_name.lower(), "uk", reversed=True)
        dob = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=65)
        notes = fake.text(max_nb_chars=100)
    # row = Contact(
    #     first_name=first_name,
    #     last_name=last_name,
    #     email=f"{first_name_translit}.{last_name_translit}@{fake.free_email_domain()}",
    #     dob=dob,
    #     notes=notes,
    #     owner=owner,
    # )
    # row.save()


# def create_authors():
#     Author.objects.all().delete()
#     with open(author_data, "r") as fa:
#         data = json.load(fa)
#
#         for item in data:
#             born_date_str = item["born_date"]
#             born_date = datetime.strptime(born_date_str, "%B %d, %Y")
#             row = Author(
#                 fullname=item["fullname"],
#                 born_date=born_date,
#                 born_location=item["born_location"],
#                 biography=item["biography"],
#             )
#             row.save()
#
#
# def create_tags():
#     tags = set()
#     Tag.objects.all().delete()
#     with open(quote_data, "r") as fq:
#         data = json.load(fq)
#
#         for item in data:
#             for name in item["tags"]:
#                 tags.add(name)
#
#     for tag in tags:
#         row = Tag(tag=tag)
#         row.save()
#
#
# def create_quotes():
#     Quote.objects.all().delete()
#
#     authors = Author.objects.all()
#     tags = Tag.objects.all()
#
#     with open(quote_data, "r") as fq:
#         data = json.load(fq)
#
#         for quote in data:
#             for author in authors:
#                 if author.fullname == quote["author"]:
#                     row = Quote(author=author, quote=quote["quote"])
#                     row.save()
#
#                     for record in quote["tags"]:
#                         for tag in tags:
#                             if tag.tag == record:
#                                 row.tags.add(tag)


if __name__ == "__main__":
    create_contacts()
    # create_authors()
    # create_tags()
    # create_quotes()

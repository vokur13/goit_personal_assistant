import os
import random
import sys

import django
from faker import Faker

sys.path.append(
    "/Users/vokur/PycharmProjects/djangoProject/personal_assistant/django_project/django_project"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from accounts.models import CustomUser
from notes.models import Tag, Note

fake = Faker("uk_UA")

NUMBER_OF_TAGS = 30
NUMBER_OF_NOTES = 50


def create_tag(number_of_tags):
    Tag.objects.all().delete()
    users = CustomUser.objects.all()
    for _ in range(number_of_tags):
        name = fake.word()
        row = Tag.objects.create(name=name, owner=random.choice(users))
        row.save()


def create_note(number_of_notes):
    Note.objects.all().delete()
    users = CustomUser.objects.all()
    tags = Tag.objects.all()
    for _ in range(number_of_notes):
        name = fake.sentence(nb_words=3)
        description = fake.sentence(nb_words=10)
        row = Note.objects.create(
            name=name,
            description=description,
            owner=random.choice(users),
        )
        row.save()
        for _ in range(3):
            row.tags.add(random.choice(tags))


if __name__ == "__main__":
    create_tag(NUMBER_OF_TAGS)
    create_note(NUMBER_OF_NOTES)

import os

from django.conf import settings
from django.db import models
from django.urls import reverse

# Near the top of the file
FILE_EXTENSION_CATEGORIES = {
    "image": ["jpg", "jpeg", "png", "gif"],
    "video": ["mp4", "mov", "avi"],
    "document": ["pdf", "doc", "docx", "txt"],
    "zip": ["zip"],
}


class UserFile(models.Model):
    file = models.FileField(upload_to="personal_assistant/")
    category = models.CharField(max_length=20, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def get_file_category(self):
        ext = os.path.splitext(self.file.name)[-1].lower()
        for category, extensions in FILE_EXTENSION_CATEGORIES.items():
            if ext in extensions:
                return category
        return "other"

    def get_absolute_url(self):
        return reverse("files:download_file", kwargs={"pk": self.pk})


# class UserFile(models.Model):
#     file = models.FileField(upload_to="personal_assistant/")
#     category = models.CharField(max_length=20, blank=True, null=True)
#     owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#
#     def get_absolute_url(self):
#         return reverse("files:download_file", kwargs={"pk": self.pk})

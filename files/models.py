from django.conf import settings
from django.db import models
from django.urls import reverse


class UserFile(models.Model):
    file = models.FileField(upload_to="personal_assistant/")
    category = models.CharField(max_length=20, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("files:download_file", kwargs={"pk": self.pk})

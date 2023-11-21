from django.conf import settings
from django.db import models


class UserFile(models.Model):
    file = models.FileField(upload_to="user_files/")
    category = models.CharField(max_length=20, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

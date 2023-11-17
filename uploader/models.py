# models.py
from django.db import models
from django.conf import settings
import os

def get_file_extension(filename):
    return os.path.splitext(filename)[1]

class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_uploads/')
    category = models.CharField(max_length=255)
    extension = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Перед збереженням файлу в базу даних витягуємо і зберігаємо його розширення
        self.extension = get_file_extension(self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file.name

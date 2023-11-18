from django.db import models
from django_project import settings


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False)

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Note(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.name

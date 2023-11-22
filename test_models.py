from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("contact_detail", kwargs={"pk": self.pk})


class Note(models.Model):
    name = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=256, null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("note_detail", kwargs={"pk": self.pk})

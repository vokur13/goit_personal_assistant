# Generated by Django 4.2.7 on 2023-11-19 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="avatar",
            field=models.URLField(blank=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-12 07:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]

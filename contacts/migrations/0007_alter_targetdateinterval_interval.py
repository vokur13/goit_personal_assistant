# Generated by Django 4.2.7 on 2023-11-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0006_targetdateinterval"),
    ]

    operations = [
        migrations.AlterField(
            model_name="targetdateinterval",
            name="interval",
            field=models.PositiveSmallIntegerField(default=7),
        ),
    ]

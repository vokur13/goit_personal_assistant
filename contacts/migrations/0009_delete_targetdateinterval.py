# Generated by Django 4.2.7 on 2023-11-14 19:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0008_targetdateinterval_owner"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TargetDateInterval",
        ),
    ]

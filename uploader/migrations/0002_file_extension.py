# Generated by Django 4.2.7 on 2023-11-16 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='extension',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
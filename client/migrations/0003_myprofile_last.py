# Generated by Django 4.1 on 2023-01-23 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0002_myprofile_gains"),
    ]

    operations = [
        migrations.AddField(
            model_name="myprofile",
            name="last",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]

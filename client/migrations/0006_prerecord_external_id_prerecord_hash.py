# Generated by Django 4.1 on 2023-02-01 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0005_myprofile_forms_1"),
    ]

    operations = [
        migrations.AddField(
            model_name="prerecord",
            name="external_id",
            field=models.CharField(blank=True, default="000000", max_length=100),
        ),
        migrations.AddField(
            model_name="prerecord",
            name="hash",
            field=models.CharField(blank=True, default="000000", max_length=100),
        ),
    ]
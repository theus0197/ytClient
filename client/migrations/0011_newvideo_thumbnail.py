# Generated by Django 4.1 on 2023-08-11 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_newvideo_userviewvideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='newvideo',
            name='thumbnail',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
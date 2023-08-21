from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class typeAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.BooleanField(default=False)


def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile =  typeAccount.objects.create(
            user=kwargs['instance']
        )
        user_profile.save()

post_save.connect(create_user_profile, sender=User)
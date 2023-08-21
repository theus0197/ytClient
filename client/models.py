from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date

# Create your models here.


class pageConfigurations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    typeConfig = models.CharField(max_length=20, blank=True)
    config = models.CharField(max_length=5000, blank=True)

class newVideo(models.Model):
    id = models.AutoField(primary_key=True)
    videocode = models.CharField(max_length=200, blank=False)
    title = models.CharField(max_length=1000, blank=False)
    thumbnail = models.CharField(default="", max_length=5000, blank=False)
    views = models.IntegerField(default=1, blank=False)
    likes = models.IntegerField(default=1, blank=False)
    createdAt = models.DateField(date.today, editable=False, blank=True)
    doublePoints = models.BooleanField(blank=False)
    valueToGain = models.FloatField(blank=False)

class userViewVideo(models.Model):
    id = models.AutoField(primary_key=True)
    videoId = models.IntegerField(blank=False)
    userId = models.IntegerField(blank=False)
    likedAt = models.DateField(default=date.today, editable=False, blank=True)

class myProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    amount = models.FloatField(null=True, blank=True, default=0)
    gains = models.IntegerField(default=0)
    last = models.CharField(max_length=30, blank=True)
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now=True, blank=True)
    password = models.CharField(max_length=30, blank=True)
    forms_1 = models.BooleanField(default=False)
    forms_phone = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'meu Perfil'
        verbose_name_plural = 'meus Perfis'

class preRecord(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=30, blank=True)
    external_id = models.CharField(max_length=100, default='000000', blank=True)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Pré Registros'
        verbose_name_plural = 'Pré Registros'

def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = myProfile.objects.create(
            user=kwargs['instance']
        )
        user_profile.save()

post_save.connect(create_user_profile, sender=User)
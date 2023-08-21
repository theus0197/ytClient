from django.contrib import admin
from . import models

# Register your models here.]
class PreTypeAccount(admin.ModelAdmin):
    list_display = ('id', 'user', 'account')

admin.site.register(models.typeAccount, PreTypeAccount)

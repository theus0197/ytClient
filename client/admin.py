from django.contrib import admin
from . import models

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'gains', 'last', 'status', 'forms_1')

class PreRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'password', 'created')

class pageConfigurations(admin.ModelAdmin):
    list_display = ('id', 'name', 'typeConfig', 'config')

class newVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'videocode', 'title', 'views','thumbnail', 'likes', 'createdAt', 'doublePoints', 'valueToGain')

class userViewVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'videoId', 'userId', 'likedAt')

admin.site.register(models.myProfile, ProfileAdmin)
admin.site.register(models.preRecord, PreRecordAdmin)
admin.site.register(models.pageConfigurations, pageConfigurations)
admin.site.register(models.newVideo, newVideoAdmin)
admin.site.register(models.userViewVideo, userViewVideoAdmin)
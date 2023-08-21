
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login', views.login_admin, name='login'),
    path('api/logout', views.logout_admin, name='logout'),
    path('users', views.users, name='users'),
    path('videos', views.videos, name='videos'),
    path('api/users', views.get_users, name='get_users'),
    path('api/v2/users', views.api_get_users, name='get_users'),
    path('api/users/create', views.create_user, name='create_user'),
    path('api/enterprise/create', views.create_enterprise, name='enterprise_user'),
    path('api/users/validate/info', views.validate_info, name='create_user'),
    path('api/enterprise/validate/info', views.validate_info_interprise, name='create_enterprise'),
    path('api/users/delete', views.delete_users, name='delete_users'),
    path('control', views.control, name='control'),
    path('api/control/save', views.save_control, name='save_control'),
    path('update/db', views.update_db),
    path('api/password', views.api_user),
    path('configs', views.panelConfig),
    path('configs/updateColors', views.updateColors),
    path('configs/videos', views.getVideoData),
    path("configs/videos/create", views.createNewVideo),
    path('configs/videos/getVideos', views.getVideos),
    path('configs/upload/', views.uploadFile, name='upload_file'),
    path('configs/updateRatelimit', views.updateConfig),
]

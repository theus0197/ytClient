
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.login_template, name='login_template'),
    path('signup', views.signup_template, name='signup_template'),
    path('api/login', views.api_login, name='api_login'),
    path('api/login/param/<str:email>&<str:password>', views.api_login_params),
    path('api/logout', views.api_logout, name='api_logout'),
    path('api/signup', views.signup),
    path('api/reset/<str:email>', views.reset_password),
    path('logout', views.api_logout, name='api_logout'),
    path('confirm/play', views.confirm_play, name='confirm_play'),
    path('draw', views.draw, name='draw'),
    path('api/draw', views.api_draw),
    path('api/confirm/forms', views.api_confirm_forms),
    path('api/confirm/forms/how', views.api_forms_how),
    path('api/webhook/status', views.webhook),
    path('api/confirm/payment', views.confirm_payment),
    path('test/webhook', views.test_webhook),
    path('videos/all', views.getAllVideos),
    path('videos/id/<str:id>', views.getVideo),
    path('videos/like/<str:id>', views.likeVideo),
    path('api/webhook/hotmart', views.webhook_handler, name='webhook'),
    path('api/first/access', views.first_access, name='first_access'),
]
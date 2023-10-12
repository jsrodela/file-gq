from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('send', views.send, name="send"),
    path('receive', views.receive, name='receive'),
    path('send_result', views.send_result, name='send_result'),
    path('api', views.api, name='api'),
    path('pre_code', views.pre_code, name='pre_code'),
    path('post_file', views.post_file, name='post_flie'),
]

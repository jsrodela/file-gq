from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('send', views.send, name="send"),
    path('receive', views.receive, name='receive'),
    path('send_result', views.send_result, name='send_result'),
]

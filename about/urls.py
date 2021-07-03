from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'about'

urlpatterns = [
    url(r'^$', views.choose_about, name="choose_about"),
]
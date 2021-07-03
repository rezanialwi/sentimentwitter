from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'contact'

urlpatterns = [
    url(r'^$', views.choose_contact, name="choose_contact"),
]
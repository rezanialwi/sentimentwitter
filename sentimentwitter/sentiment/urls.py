from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'sentiment'

urlpatterns = [
    url(r'^$', views.sentiment_analysis, name="sentiment_anaylsis"),
    url(r'^type/$', views.sentiment_analysis_type, name="sentiment_analysis_type"),
    url(r'^import/$', views.sentiment_analysis_import, name="sentiment_analysis_import"),
]


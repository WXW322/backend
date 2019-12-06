from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^queryProSummary/', views.getDatas),
    url(r'^getProtoDataDetail/', views.getProtoDataDetail),
    url(r'^querySplitSummary/', views.getProtoSplitSummary),
    url(r'^getSplitProtoDataDetail/', views.getSplitProtoDataDetail),
    url(r'^queryIcsFieldTypes/', views.getIcsFieldTypes)
]
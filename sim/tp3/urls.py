from django.contrib import admin
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.index_view, name="index"),
    re_path(r'^tp3/?$', views.tp3_view, name="tp3_view"),
]
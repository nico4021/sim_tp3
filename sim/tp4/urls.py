from django.contrib import admin
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    re_path(r'^tp4/?$', views.tp4_view, name="tp4_view"),
]
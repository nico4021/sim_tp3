from django.contrib import admin
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    re_path(r'^tp2/?$', views.tp2_view, name="tp2_view"),
    re_path(r'^tp2/poisson/?$', views.tp2_poisson, name="tp2_poisson"),
    re_path(r'^tp2/normal/?$', views.tp2_normal, name="tp2_normal"),
    re_path(r'^tp2/uniforme/?$', views.tp2_uniforme, name="tp2_uniforme"),
    re_path(r'^tp2/exponencial/?$', views.tp2_exponencial, name="tp2_exponencial"),
]
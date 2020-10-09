from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('data/aggregated/', views.data.aggregated),
    path('data/distributed/', views.data.distributed),
    path('tags/', views.tags),
]

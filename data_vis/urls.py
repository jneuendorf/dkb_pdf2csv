from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='data'),
    path('data_raw/', views.data_raw, name='data_raw'),
    path('tags/', views.tags, name='tags'),
]

from django.urls import path

from .views import index, test, api


urlpatterns = [
    path('', index),
    path('test/', test),
    path('api/data/aggregated/', api.data.aggregated),
    path('api/data/distributed/', api.data.distributed),
    path('api/tags/', api.tags),
    path('api/analytics/finders/', api.analytics.finders),
]

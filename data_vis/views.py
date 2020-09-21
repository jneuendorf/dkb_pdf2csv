# from typing import List, Iterable

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from .models import Series


def index(request: HttpRequest):
    return render(request, 'data_vis/index.html', {})


def data(request: HttpRequest):
    series_names = request.GET.getlist('series', default=[])
    start = request.GET.get('start', default='1970-01-01')
    end = request.GET.get('end', default='9999-12-31')

    if not series_names:
        series = Series.objects.all()
    else:
        series = Series.objects.filter(name__in=series_names)

    return JsonResponse({
        s.name: {
            'initial_value': s.initial_value,
            'data_points': [
                (point.x, point.dy)
                for point in s.data_points.filter(x__gte=start, x__lte=end)
            ],
        }

        for s in series
    })

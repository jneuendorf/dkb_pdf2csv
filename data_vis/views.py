from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from .models import Series
from . import utils


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

    series_data = []
    for s in series:
        series_data.append({
            'id': s.name,
            'data': utils.data.accumulated(s, start, end),
        })

    return JsonResponse(series_data, safe=False)

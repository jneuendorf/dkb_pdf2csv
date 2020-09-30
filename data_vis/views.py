from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from .models import Series, Tag
from .serializers import JsonEncoder
from . import utils


def index(request: HttpRequest):
    return render(request, 'data_vis/index.html', {})


def data_raw(request: HttpRequest):
    start = request.GET.get('start', default='1970-01-01')
    end = request.GET.get('end', default='9999-12-31')

    series = Series.objects.all()
    series_data = []
    for s in series:
        data = utils.data.limited(s, start, end)
        series_data.append({
            'id': s.name,
            'data': data,
        })

    return JsonResponse(series_data, encoder=JsonEncoder, safe=False)


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

    return JsonResponse(series_data, encoder=JsonEncoder, safe=False)


def tags(request: HttpRequest):
    return JsonResponse(
        list(Tag.objects.values('identifier', 'is_abstract')),
        encoder=JsonEncoder,
        safe=False,
    )

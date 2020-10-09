from django.http import JsonResponse
from typing import Iterable

from .. import utils
from ..models import DataPoint, Series
from .serializers import JsonEncoder


# def data_raw(request: HttpRequest):
#     start = request.GET.get('start', default='1970-01-01')
#     end = request.GET.get('end', default='9999-12-31')
#
#     series = Series.objects.all()
#     series_data = []
#     for s in series:
#         data = utils.data.limited(s, start, end)
#         series_data.append({
#             'id': s.name,
#             'data': data,
#         })
#
#     return JsonResponse(series_data, encoder=JsonEncoder, safe=False)


def limited_series(request) -> Iterable[Iterable[DataPoint]]:
    series_names = request.GET.getlist('series', default=[])
    start = request.GET.get('start', default='1970-01-01')
    end = request.GET.get('end', default='9999-12-31')

    if not series_names:
        series = Series.objects.all()
    else:
        series = Series.objects.filter(name__in=series_names)

    return [
        (s, s.data_points.filter(x__gte=start, x__lte=end))
        for s in series
    ]


def aggregated(request):
    series_data = []
    for series, limited_points in limited_series(request):
        series_data.append({
            'id': series.name,
            'data': utils.data.aggregated(series, limited_points),
        })

    return JsonResponse(series_data, encoder=JsonEncoder, safe=False)


def distributed(request):
    series_data = []
    for series, limited_points in limited_series(request):
        series_data.append({
            'id': series.name,
            'data': utils.data.distributed(series, limited_points),
        })

    return JsonResponse(series_data, encoder=JsonEncoder, safe=False)

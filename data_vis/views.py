from collections import defaultdict

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

    series_data = []
    for s in series:
        points_by_date = defaultdict(list)
        # y = s.initial_value
        for point in s.data_points.filter(x__gte=start, x__lte=end):
            # next_y = y + point.dy
            points_by_date[point.x.date()].append(dict(
                dy=point.dy,
                meta=point.meta,
            ))
            # points_by_date.append(dict(
            #     x=point.x,
            #     y=next_y,
            #     meta=point.meta,
            # ))
            # y = next_y

        s_data = []
        y = s.initial_value
        for date in sorted(points_by_date.keys()):
            points = points_by_date[date]
            next_y = y + sum(point['dy'] for point in points)
            aggregated_point = dict(
                x=date.strftime('%Y-%m-%d'),
                y=next_y,
                meta=', '.join(point['meta'] for point in points)
            )
            s_data.append(aggregated_point)

            y = next_y

        series_data.append({
            'id': s.name,
            # 'color': '',
            'data': s_data,
        })

    return JsonResponse(series_data, safe=False)

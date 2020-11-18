import json
from typing import List

from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

from data_analysis.pattern_finders.frequency import FrequencyPatternFinder
from .data import limited_series
from .serializers import JsonEncoder


# @csrf_exempt
def finders(request):
    if 'start' not in request.GET or 'end' not in request.GET:
        raise ValueError('Missing GET param "start" or "end"')

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # print(body)

    if body:
        # FIELD_NAMES = ('id', 'x', 'dy')
        FIELD_NAMES = ('id',)
        finders: List[FrequencyPatternFinder] = [
            FrequencyPatternFinder(**kwargs)
            for kwargs in body
        ]
        patterns_by_series = {}
        for series, data_points_queryset in limited_series(request):
            # print('??', data_points_queryset)
            for finder in finders:
                patterns = finder.find(data_points_queryset)
                # print('??', patterns)
                patterns_by_series[series.name] = [
                    [
                        point.as_dict(field_names=FIELD_NAMES)
                        for point in pattern
                    ]
                    for pattern in patterns
                ]

        return JsonResponse(
            patterns_by_series,
            encoder=JsonEncoder,
            # safe=False,
        )
    else:
        raise ValueError('No request body given')

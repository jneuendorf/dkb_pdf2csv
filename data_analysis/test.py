from datetime import datetime
from pprint import pprint

from iterable_orm import QuerySet

from data_analysis.pattern_finders.frequency import FrequencyPatternFinder
from data_vis.models import Series, DataPoint


# from data_analysis.test import *

data_points = QuerySet([
    DataPoint(x=datetime(2020, 1, 1), dy=100),
    DataPoint(x=datetime(2020, 1, 1), dy=-100),
    DataPoint(x=datetime(2020, 1, 4), dy=2),
    DataPoint(x=datetime(2020, 2, 1), dy=95),
    DataPoint(x=datetime(2020, 2, 5), dy=200),
    # DataPoint(x=datetime(2020, 3, 1), dy=105),
    DataPoint(x=datetime(2020, 4, 4), dy=-4),
])


# TODO: make real tests
def f():
    series = Series.objects.first()
    finder = FrequencyPatternFinder(intervals=[dict(weeks=1)])
    subsets = finder.find(series.data_points.filter(x__lte='2020-04-01'))
    pprint(subsets)


def g():
    finder = FrequencyPatternFinder(
        intervals=[dict(months=1)],
        tolerance_y=10,
    )
    series = Series.objects.first()
    # patterns = finder.find(series.data_points.filter(x__lte='2020-03-01'))
    patterns = finder.find(data_points)
    pprint(patterns)

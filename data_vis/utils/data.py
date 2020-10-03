from collections import defaultdict
from datetime import date as Date, timezone as Timezone
from functools import partial
from typing import Iterable, Tuple, List, TypedDict, Set


class PointNoX(TypedDict):
    dy: float
    meta: str


class Point(TypedDict):
    x: str
    dy: float
    meta: str


def limited(series, start, end):
    j = 0
    last_date = None

    def transform_x(i, x):
        nonlocal last_date, j
        if x.date() == last_date:
            last_date = x.date()
            j += 1
        else:
            j = 0
        return x.replace(minute=j, tzinfo=Timezone.utc).isoformat()
    # transformers = dict(
    #     # x=lambda x: x.date(),
    #     x=lambda x: x.replace().isoformat(),
    # )
    return sorted(
        [
            # point.as_dict(transformers)
            point.as_dict(x=partial(transform_x, i))
            for i, point in enumerate(
                series.data_points.filter(x__gte=start, x__lte=end)
            )
        ],
        key=lambda item: item['x']
    )


def grouped_by_date(series, start, end) -> Iterable[Tuple[Date, PointNoX]]:
    points_by_date = defaultdict(list)
    for point in series.data_points.filter(x__gte=start, x__lte=end):
        points_by_date[point.x.date()].append(point)
    return list(sorted(points_by_date.items(), key=lambda item: item[0]))


def aggregate_points(points):
    return dict(
        x=points[0].x.date(),
        dy=sum(point.dy for point in points),
        meta='; '.join([
            f"{point.meta} ({str(point.dy)})"
            for point in points
        ]),
        tags=set(
            tag.identifier
            for point in points
            for tag in point.tags.all()
        ),
    )


def accumulated(series,
                start='1970-01-01',
                end='9999-12-31') -> Tuple[List[Point], Set[str]]:
    series_data = []
    y = series.initial_value
    # for date, points in grouped_by_date(series, start, end):
    #     aggregated_point = aggregate_points(points)
    #     aggregated_point['x'] = aggregated_point['x'].strftime('%Y-%m-%d')
    #     aggregated_point['y'] = aggregated_point.pop('dy')
    #     next_y = round(y + aggregated_point['y'], 2)
    #     series_data.append(aggregated_point)
    #
    #     y = next_y
    for point in limited(series, start, end):
        point['y'] = round(y + point['dy'], 2)
        series_data.append(point)

        y = point['y']

    return series_data

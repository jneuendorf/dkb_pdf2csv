from collections import defaultdict
from datetime import timezone as Timezone
from typing import Iterable, List, TypedDict


class Point(TypedDict):
    x: str
    y: float
    dy: float
    meta: str


# def limited(series, start, end):
#     def transform_x(x):
#         return x.replace(tzinfo=Timezone.utc).isoformat()
#
#     return sorted(
#         [
#             point.as_dict(x=transform_x)
#             for i, point in enumerate(
#                 series.data_points.filter(x__gte=start, x__lte=end)
#             )
#         ],
#         key=lambda item: item['x']
#     )


# TODO: use itertools.groupby?!
def grouped_points(points,
                   key=lambda p: p.x.date()) -> Iterable[List[Point]]:
    """Groups points within the date range by the 'key' argument."""

    points_by_date = defaultdict(list)
    for point in points:
        points_by_date[key(point)].append(point)
    return sorted(
        points_by_date.values(),
        key=lambda points: key(points[0]),
    )


def distributed_grouped(grouped) -> List[Point]:
    """Evenly distributes points in the same group across the day
    (rounded to minutes).

    Example: If there are 3 points for one date 2020-01-01, those 3 points will
    be assigned the datetimes
    - 2020-01-01T00:00:00
    - 2020-01-01T08:00:00
    - 2020-01-01T16:00:00
    """

    MINUTES_PER_DAY = 24 * 60

    points = []
    for _, group in grouped:
        group_size = len(group)
        space_in_minutes = MINUTES_PER_DAY // group_size
        used_minutes = 0
        for point in group:
            hour, minute = divmod(used_minutes, 60)
            points.append(point.as_dict(
                x=lambda x: (
                    point.x
                    .replace(
                        hour=hour,
                        minute=minute,
                        tzinfo=Timezone.utc,
                    )
                    .isoformat()
                )
            ))
            used_minutes += space_in_minutes
    return points


def aggregate_points(points):
    return dict(
        x=points[0].x.date().strftime('%Y-%m-%d'),
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


def aggregated(series, limited_points) -> List[Point]:
    series_data = []
    y = series.initial_value
    for _, points in grouped_points(limited_points):
        point = aggregate_points(points)
        point['y'] = round(y + point['dy'], 2)
        series_data.append(point)
        y = point['y']

    return series_data


def distributed(series, limited_points) -> List[Point]:
    series_data = []
    y = series.initial_value
    for point in distributed_grouped(grouped_points(limited_points)):
        point['y'] = round(y + point['dy'], 2)
        series_data.append(point)
        y = point['y']

    return series_data

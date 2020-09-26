from collections import defaultdict
from datetime import date as Date
from typing import Iterable, Tuple, List, TypedDict


class PointNoX(TypedDict):
    dy: float
    meta: str


class Point(TypedDict):
    x: str
    dy: float
    meta: str


def grouped_by_date(series, start, end) -> Iterable[Tuple[Date, PointNoX]]:
    points_by_date = defaultdict(list)
    for point in series.data_points.filter(x__gte=start, x__lte=end):
        points_by_date[point.x.date()].append(point.as_dict())
    return sorted(points_by_date.items(), key=lambda item: item[0])


def accumulated(series, start='1970-01-01', end='9999-12-31') -> List[Point]:
    series_data = []
    y = series.initial_value
    for date, points in grouped_by_date(series, start, end):
        next_y = round(y + sum(point['dy'] for point in points), 2)
        aggregated_point = dict(
            x=date.strftime('%Y-%m-%d'),
            y=next_y,
            meta='; '.join([
                f"{point['meta']} ({str(point['dy'])})"
                for point in points
            ]),
            tags=list(set(
                tag_identifier
                for point in points
                for tag_identifier in point['tags']
            )),
        )
        series_data.append(aggregated_point)

        y = next_y

    return series_data

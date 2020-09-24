import csv
from io import StringIO

from ..models import DataPoint


def series_to_csv(series):
    points = series.data_points.all().order_by('x')
    point_dicts = (point.as_dict() for point in points)

    in_memory_csv = StringIO()
    writer = csv.DictWriter(
        in_memory_csv,
        fieldnames=DataPoint.CSV_FIELD_NAMES,
    )
    writer.writeheader()
    writer.writerows(point_dicts)

    csv_data = in_memory_csv.getvalue()
    in_memory_csv.close()

    return (f'{series.name}.csv', csv_data)

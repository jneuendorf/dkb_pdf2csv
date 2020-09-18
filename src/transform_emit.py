import csv
from typing import List

from .row import Row, HeaderRow


def transform_emit(pdf: str, header_row: HeaderRow, rows: List[Row]):
    # No transform

    with open(f'{pdf}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header_row.get_texts())
        writer.writeheader()
        writer.writerows([
            row.as_dict(header_row)
            for row in rows
        ])

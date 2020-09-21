import csv
from typing import List

from .row import Row, HeaderRow


def transform_emit(pdf: str, header_row: HeaderRow, rows: List[Row],
                   rows_by_page: List[List[Row]],
                   callback_args: list):
    # No transform

    with open(f'{pdf}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header_row.get_texts())
        writer.writeheader()
        writer.writerows([
            row.as_dict(header_row)
            for row in rows
        ])

from datetime import datetime


def parse_german_float(n: str) -> float:
    return float(n.replace('.', '').replace(',', '.'))


def parse_german_date(date_string, with_year=False) -> datetime:
    format = '%d.%m.%Y' if with_year else '%d.%m.'
    return datetime.strptime(date_string, format)


def with_datetimes(date_range, row_dicts, key='Wert'):
    """Returns a new list with row dicts whose key 'key' is replaced with
    the parsed date including the correct year according to the date range.
    """

    start, end = date_range
    start_year = start.year
    end_year = end.year

    assert start_year <= end_year, 'Invalid date range'

    year = start_year
    row_dicts_with_datetimes = []
    prev_month = 0
    for row_dict in row_dicts:
        assert year <= end_year, f'Year out or range (date {row_dict[key]})'

        date = parse_german_date(row_dict[key])
        current_month = date.month
        row_dicts_with_datetimes.append({
            **row_dict,
            key: date.replace(year=year),
        })
        if prev_month > current_month:
            year += 1
        prev_month = current_month

    return row_dicts_with_datetimes

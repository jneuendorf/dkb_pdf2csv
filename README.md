# dkb_pdf2csv

`pipenv run python main.py ./sample.pdf `


## Installation

- `brew install libmagic` for [python-magic](https://pypi.org/project/python-magic/)


## Process

1. Parse the PDF file into a list of table rows (data).
2. Optionally, transform the data.
3. Optionally, emit the data to some output (e.g. a file).

This process can be configured:

1. The parser takes some configuration kwargs.
2. You can specify a function `transform_emit: Callable[[List[Row]], Any]` to process and/or
   output the data. By default, the data is not transformed and emitted into
   a CSV file with the same name as the input PDF file.


## Configuration

`config.py`

```python
def transform_emit(rows: List[Row]):
    ...

config = dict(
    parser=dict(
        column_types=None,
        alignment=None,
        header_row_label=None,
        column_x_tolerance=1,
        max_missing_cells_per_row=1,
    ),
    transform_emit=transform_emit,
)
```

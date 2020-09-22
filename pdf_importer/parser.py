from collections import defaultdict
from dataclasses import dataclass, field
# import logging
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

from pdfminer.high_level import extract_pages
import pdfminer.layout as layout

from .types import Type
from .row import Row, HeaderRow


DEFAULT_COLUMN_TYPE: Type = str

# TODO: Use verbose debug logging
# logger = logging.getLogger(__name__)


@dataclass
class Parser:
    """Parses a single pdf file into a table like structure.

    Attributes:
        pdf
        alignment
        header_row_labels
        max_missing_cells_per_row
    """

    pdf: str
    alignment: Optional[str] = None
    header_row_labels: Optional[List[str]] = None
    column_x_tolerance: float = 1.0
    max_missing_cells_per_row: int = 1
    """Number of cells that may be missing in a row. Rows with less elements
    are not considered rows of the table and disregarded.
    """

    _implied_num_columns: Optional[int] = field(init=False)
    _header_row_kwargs: Dict[str, Any] = field(init=False)
    _row_kwargs: Dict[str, Any] = field(init=False)

    def __post_init__(self):
        custom_attrs = []

        if self.alignment is not None:
            custom_attrs.append(self.alignment)
        if self.header_row_labels is not None:
            custom_attrs.append(self.header_row_labels)

        self._implied_num_columns = None
        if len(custom_attrs) > 0:
            lengths = [len(attr) for attr in custom_attrs]
            if len(set(lengths)) == 1:
                self._implied_num_columns = lengths[0]
            else:
                raise ValueError(
                    'Some arguments\' lenghts do not match. Make sure '
                    '"alignment" and "header_row_labels" have the same length!'
                )

        self._header_row_kwargs = dict(
            custom_labels=self.header_row_labels,
        )
        self._row_kwargs = dict(
            tolerance=self.column_x_tolerance,
        )

    def parse(self) -> Tuple[HeaderRow, List[Row]]:
        # Save each page separately.
        # This way, we avoid e.g. footer addresses to add over pages
        # because they always have the same coordinates.
        pages: List[List[Row]] = []

        for page_layout in extract_pages(self.pdf):
            rows = defaultdict(list)
            for element in page_layout:
                # Basically LTChar and LTTextContainer + subclasses.
                # <=> subclass of LTText without LTAnno
                is_positioned_text = (
                     isinstance(element, layout.LTText)
                     and isinstance(element, layout.LTComponent)
                )
                if is_positioned_text:
                    # TODO: Make range configurable. Rounding means buckets
                    # with size 1 but maybe one needs more
                    # (x1, y1) is the top-right and we need to top coordinate
                    rows[int(element.y1)].append(element)

            # Making sure we append rows from top to bottom
            # (thus sorting descending by y1).
            pages.append([
                Row(row_cells, **self._row_kwargs)
                for y1, row_cells in sorted(
                    rows.items(),
                    key=lambda tup: tup[0],
                    reverse=True,
                )
            ])

        header_row = HeaderRow(pages, **self._header_row_kwargs)
        detected_num_columns = len(header_row)

        if (
            self._implied_num_columns is not None
            and detected_num_columns != self._implied_num_columns
        ):
            raise ValueError(
                f'Detected {detected_num_columns} columns but '
                f'your arguments imply {self._implied_num_columns} column(s).'
            )
        else:
            num_columns = detected_num_columns

        table_rows = []
        for i, rows in enumerate(pages):
            for row in rows:
                if len(row) >= num_columns - self.max_missing_cells_per_row:
                    if row != header_row:
                        table_rows.append(row)

        return header_row, table_rows, pages

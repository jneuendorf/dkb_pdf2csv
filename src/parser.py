from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from pdfminer.high_level import extract_pages
import pdfminer.layout as layout

from .types import Type
from .row import Row, HeaderRow


DEFAULT_COLUMN_TYPE: Type = str


@dataclass
class Parser:
    """Parses a single pdf file into a table like structure.

    Attributes:
        pdf
        column_types: Optional[
        alignment:
        header_row_labels: Optional[
        max_missing_cells_per_row: int = 1
    """

    pdf: str
    column_types: Optional[List[Type]] = None
    alignment: Optional[str] = None
    header_row_labels: Optional[List[str]] = None
    column_x_tolerance: int = 1
    max_missing_cells_per_row: int = 1
    """Number of cells that may be missing in a row. Rows with less elements
    are not considered rows of the table and disregarded.
    """

    _implied_num_columns: Optional[int] = field(init=False)
    _header_row_kwargs: Dict[str, Any] = field(init=False)
    _row_kwargs: Dict[str, Any] = field(init=False)

    def __post_init__(self):
        custom_attrs = []

        if self.column_types is not None:
            custom_attrs.append(self.column_types)
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
                    'Some arguments\' lenghts do not match. '
                    'Make sure "column_types", "alignment" and '
                    '"header_row_labels" have the same length!'
                )

        self._header_row_kwargs = dict(
            custom_labels=self.header_row_labels,
        )
        self._row_kwargs = dict(
            tolerance=self.column_x_tolerance,
        )


    def parse(self, pdf: str):
        # Save each page separately.
        # This way, we avoid e.g. footer addresses to add over pages
        # because they always have the same coordinates.
        pages: List[List[Row]] = []

        for page_layout in extract_pages(pdf):
            rows = defaultdict(list)
            for element in page_layout:
                # Basically LTChar and LTTextContainer + subclasses.
                # <=> subclass of LTText without LTAnno
                is_positioned_text = (
                     isinstance(element, layout.LTText)
                     and isinstance(element, layout.LTComponent)
                )
                if is_positioned_text:
                    # (x1, y1) is the top-right and we need to top coordinate
                    rows[element.y1].append(element)
            # pages.append(rows)
            pages.append([
                Row(row_cells, **self._row_kwargs)
                for row_cells in rows.values()
            ])

        header_row = self.get_header_row(pages)
        detected_num_columns = len(header_row)

        if (
            self._implied_num_columns is not None
            and detected_num_columns != self._implied_num_columns
        ):
            raise ValueError(
                f'Detected {detected_num_columns} columns but '
                f'your arguments imply {self._implied_num_columns} columns.'
            )
        else:
            num_columns = detected_num_columns

        header_row_labels = header_row.get_texts()
        # if self.header_row_labels is None:
        #     header_row_labels = header_row.get_texts()
        # else:
        #     header_row_labels = self.header_row_labels

        HEADER_ROW_LABELS_BY_X = {
            # left x coordinates
            **{
                cell.x0: header_row_labels[i]
                for i, cell in enumerate(header_row)
            },
            # right x coordinates
            **{
                cell.x1: header_row_labels[i]
                for i, cell in enumerate(header_row)
            },
        }

        for i, rows in enumerate(pages):
            for row in rows:
                if len(row) >= num_columns - self.max_missing_cells_per_row:
                    if row != header_row:
                        print(row.as_dict(header_row))
                        # print(get_row_dict(HEADER_ROW_LABELS_BY_X, row))
                        print()

    def get_header_row(self, pages) -> HeaderRow:
        """Look for number of columns of the table.
        Assuming that the header row has the greatest number of elements
        with the same top-y value.
        We also assume the table has the same structure across all pages
        and starts on the 1st page.
        """
        header_cells = []
        for y, elements in pages[0].items():
            if len(elements) > len(header_cells):
                header_cells = elements

        return HeaderRow(header_cells, **self._header_row_kwargs)

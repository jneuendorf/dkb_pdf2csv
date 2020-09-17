from collections import defaultdict
from typing import List, DefaultDict, Dict

from pdfminer.high_level import extract_pages
import pdfminer.layout as layout


# Types
Element = layout.LTText
Rows = DefaultDict[float, List[Element]]


# Save each page separately.
# This way, we avoid e.g. footer addresses to add over pages
# because they always have the same coordinates.
page_elements: List[Rows] = []

for page_layout in extract_pages("sample.pdf"):
    rows: Rows = defaultdict(list)
    for element in page_layout:
        # Basically LTChar and LTTextContainer + subclasses.
        # <=> subclass of LTText without LTAnno
        is_text_and_component = (
             isinstance(element, layout.LTText)
             and isinstance(element, layout.LTComponent)
        )
        if is_text_and_component:
            # (x1, y1) is the top-right and we need to top coordinate
            rows[element.y1].append(element)
    page_elements.append(rows)


def get_header_row(page_elements) -> List[Element]:
    """
    Look for number of columns of the table.
    Assuming that the header row has the greatest number of elements
    with the same top-y value.
    We also assume the table has the same structure across all pages
    and starts on the 1st page.
    """
    header_row = []
    for y, elements in page_elements[0].items():
        if len(elements) > len(header_row):
            header_row = elements

    return header_row


def get_texts(row) -> List[str]:
    return [cell.get_text().strip() for cell in row]


def get_row_dict(header_row_labels_by_x, row, tolerance=1) -> Dict[float, str]:
    """
    Since a row can miss a cell in the middle,
    we cannot just use the indices to map to columns.
    Therefore, we try to match either the left x (x0)
    or the right x (x1) coordinate.
    """

    row_dict = {}
    for i, cell in enumerate(row):
        cell_text = cell.get_text().strip()
        if cell.x0 in header_row_labels_by_x:
            row_dict[cell.x0] = cell_text
        elif cell.x1 in header_row_labels_by_x:
            row_dict[cell.x1] = cell_text
        else:
            x0s_in_tolerance = [
                x for x in header_row_labels_by_x.keys()
                if abs(x - cell.x0) <= tolerance
            ]
            x1s_in_tolerance = [
                x for x in header_row_labels_by_x.keys()
                if abs(x - cell.x1) <= tolerance
            ]
            # If there is only one distinct value within the tolerance,
            # we take it (as we prefer left alignment just like above).
            if len(x0s_in_tolerance) == 1:
                row_dict[x0s_in_tolerance[0]] = cell_text
            # Try right alignment.
            elif len(x1s_in_tolerance) == 1:
                row_dict[x1s_in_tolerance[0]] = cell_text
            else:
                print('cell index =', i)
                raise ValueError(
                    f'Could not associate cell {str(cell)} with a column.'
                )

    return {
        header_row_labels_by_x[x]: text
        for x, text in row_dict.items()
    }
    # return row_dict


# ALIGNMENT = {
#     'Bu.Tag': 'l',
#     'Wert': 'l',
#     'Wir haben für Sie gebucht': 'l',
#     'Belastung in EUR': 'r',
#     'Gutschrift in EUR': 'r',
# }
# TODO: Class 'HeaderRow'
HEADER_ROW = get_header_row(page_elements)
HEADER_ROW_TEXTS = get_texts(HEADER_ROW)
HEADER_ROW_LABELS_BY_X = {
    **{
        cell.x0: cell.get_text().strip()
        for cell in HEADER_ROW
    },
    **{
        cell.x1: cell.get_text().strip()
        for cell in HEADER_ROW
    },
}
N_COLS = len(HEADER_ROW)

print()
print()
# print(HEADER_ROW)
print(HEADER_ROW_TEXTS)
print()
print(HEADER_ROW_LABELS_BY_X)
print()
print()


for i, rows in enumerate(page_elements):
    for y, row in rows.items():
        if len(row) >= N_COLS - 1:
            row_texts = get_texts(row)
            if row_texts != HEADER_ROW_TEXTS:
                # print(row_texts)
                print(get_row_dict(HEADER_ROW_LABELS_BY_X, row))
                print()

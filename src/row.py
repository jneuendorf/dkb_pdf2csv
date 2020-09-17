from typing import List

from .types import Element


class Row:
    cells: List[Element]

    def __init__(self, cells):
        self.cells = cells

    def get_texts(self) -> List[str]:
        return [cell.get_text().strip() for cell in self]

    def as_dict(self, header_row: "HeaderRow"):
        """
        Since a row can miss a cell in the middle,
        we cannot just use the indices to map to columns.
        Therefore, we try to match either the left x (x0)
        or the right x (x1) coordinate.
        """

        header_row_labels_by_x = self.get_labels_by_x()
        row_dict = {}
        for i, cell in enumerate(self.cells):
            cell_text = cell.get_text().strip()
            matched_x = None
            if cell.x0 in header_row_labels_by_x:
                matched_x = cell.x0
            elif cell.x1 in header_row_labels_by_x:
                matched_x = cell.x1
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
                    matched_x = x0s_in_tolerance[0]
                # Try right alignment.
                elif len(x1s_in_tolerance) == 1:
                    matched_x = x1s_in_tolerance[0]
                else:
                    print('cell index =', i)
                    raise ValueError(
                        f'Could not associate cell {str(cell)} with a column.'
                    )

            if matched_x is not None:
                row_dict[header_row_labels_by_x[matched_x]] = cell_text

        return row_dict

    def __len__(self):
        return len(self.cells)

    def __eq__(self, row):
        return isinstance(row, Row) and self.get_texts() == row.get_texts()

    # @property
    # def y_top(self):
    #     return self.cells[0].y1


class HeaderRow(Row):

    def __init__(self, pages, header_row_labels=None):
        header_cells = []
        for elements in pages[0]:
            if len(elements) > len(header_cells):
                header_cells = elements

        super().__init__(header_cells)
        self.header_row_labels = header_row_labels

        # self.header_row_labels = (
        #     header_row_labels
        #     if header_row_labels is not None
        #     else super().get_texts()
        # )
    # def __init__(self, cells, header_row_labels=None):
    #     super().__init__(cells)
    #     self.header_row_labels = (
    #         header_row_labels
    #         if header_row_labels is not None
    #         else super().get_texts()
    #     )

    def get_texts(self):
        return (
            self.header_row_labels
            if self.header_row_labels is not None
            else super().get_texts()
        )
    # def get_texts(self):
    #     return self.header_row_labels

    def get_labels_by_x(self):
        header_row_labels = self.get_texts()
        return {
            # left x coordinates
            **{
                cell.x0: header_row_labels[i]
                for i, cell in enumerate(self.cells)
            },
            # right x coordinates
            **{
                cell.x1: header_row_labels[i]
                for i, cell in enumerate(self.cells)
            },
        }

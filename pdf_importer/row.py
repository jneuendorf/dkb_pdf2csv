from typing import List, Dict, Any

from .types import Element


class Row:
    cells: List[Element]
    options: Dict[str, Any]

    def __init__(self, cells, **options):
        self.cells = cells
        self.options = options

    def get_texts(self) -> List[str]:
        return [cell.get_text().strip() for cell in self.cells]

    def get_text(self, sep: str = '') -> str:
        return sep.join(self.get_texts())

    def as_dict(self, header_row: "HeaderRow"):
        """
        Since a row can miss a cell in the middle,
        we cannot just use the indices to map to columns.
        Therefore, we try to match either the left x (x0)
        or the right x (x1) coordinate.
        """

        header_row_labels_by_x = header_row.get_labels_by_x()
        row_dict = {}
        for i, cell in enumerate(self.cells):
            cell_text = cell.get_text().strip()
            matched_x = None
            if cell.x0 in header_row_labels_by_x:
                matched_x = cell.x0
            elif cell.x1 in header_row_labels_by_x:
                matched_x = cell.x1
            else:
                # TODO: Check if 'tolerance' in self.options
                x0s_in_tolerance = [
                    x for x in header_row_labels_by_x.keys()
                    if abs(x - cell.x0) <= self.options['tolerance']
                ]
                x1s_in_tolerance = [
                    x for x in header_row_labels_by_x.keys()
                    if abs(x - cell.x1) <= self.options['tolerance']
                ]
                # If there is only one distinct value within the tolerance,
                # we take it (as we prefer left alignment just like above).
                if len(x0s_in_tolerance) == 1:
                    matched_x = x0s_in_tolerance[0]
                # Try right alignment.
                elif len(x1s_in_tolerance) == 1:
                    matched_x = x1s_in_tolerance[0]
                else:
                    raise ValueError(
                        f'Could not associate cell {str(cell)} at '
                        f'positition {i} ''with a column.'
                    )

            if matched_x is not None:
                row_dict[header_row_labels_by_x[matched_x]] = cell_text

        return row_dict

    def __len__(self):
        return len(self.cells)

    def __eq__(self, row):
        return isinstance(row, Row) and self.get_texts() == row.get_texts()

    def __str__(self):
        texts = self.get_texts()
        return f'<{self.__class__.__name__} {str([text for text in texts])}>'

    # @property
    # def y_top(self):
    #     return self.cells[0].y1


class HeaderRow(Row):

    def __init__(self, pages, **options):
        """Look for number of columns of the table.
        Assuming that the header row has the greatest number of elements
        with the same top-y value.
        We also assume the table has the same structure across all pages
        and starts on the 1st page.
        """
        header_cells = []
        for row in pages[0]:
            if len(row) > len(header_cells):
                header_cells = row.cells

        super().__init__(header_cells, **options)

    def get_texts(self):
        return (
            self.options['custom_labels']
            if self.options['custom_labels'] is not None
            else super().get_texts()
        )

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

    def __eq__(self, row):
        """Compares also the cell texts in case self.options['custom_label']
        is set. If there are custom labels the header row read from the PDF
        still contains the original labels which the HeaderRow instance knows
        because the original cells are still associated.
        """
        return super().__eq__(row) or Row(self.cells) == row

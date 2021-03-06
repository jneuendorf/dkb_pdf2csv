from datetime import datetime
import re
from typing import List, Tuple

from django.conf import settings
from django.db import models, transaction

from data_vis.models import DataPoint, PdfFile
from data_vis.utils import pdf_import
from pdf_importer.process import Process
from pdf_importer.row import Row, HeaderRow


class Series(models.Model):
    name = models.CharField(max_length=100)
    initial_value = models.FloatField(default=0)

    def import_pdfs(self, pdf_filenames: List[str], pdfs: List[PdfFile]):
        process = Process(config=dict(
            parser=getattr(settings, 'DATA_VIS_PARSE_OPTIONS', {}),
            transform_emit=self.transform_emit,
        ))
        process.run(pdf_filenames, transform_emit_args=pdfs)

    def transform_emit(self,
                       pdf_filename: str,
                       header_row: HeaderRow,
                       rows: List[Row],
                       rows_by_page: List[List[Row]],
                       pdf: PdfFile):
        date_range_text = [
            row.get_text()
            for row in rows_by_page[0]
            if len(row) == 1 and 'Kontoauszug' in row.get_text()
        ][0]
        pattern = (
            r'^Kontoauszug Nummer \d{3} / \d{4} vom '
            r'(\d{2}\.\d{2}\.\d{4}) bis (\d{2}\.\d{2}\.\d{4})'
        )
        match = re.match(pattern, date_range_text)
        date_range = [
            pdf_import.parse_german_date(date, with_year=True)
            for date in match.group(1, 2)
        ]

        data_points = self.transform_rows(header_row, rows, date_range)

        with transaction.atomic():
            self.data_points.bulk_create(data_points)
            pdf.is_imported = True
            pdf.save()

    def transform_rows(self, header_row: HeaderRow, rows: List[Row],
                       date_range: Tuple[datetime]) -> List:
        row_dicts = pdf_import.with_datetimes(
            date_range,
            [row.as_dict(header_row) for row in rows],
        )
        return [
            DataPoint(
                series=self,
                x=row_dict['Wert'],
                dy=(
                    -1 * pdf_import.parse_german_float(
                        row_dict['Belastung in EUR'],
                    )
                    if 'Belastung in EUR' in row_dict
                    else pdf_import.parse_german_float(
                        row_dict['Gutschrift in EUR'],
                    )
                ),
                meta=row_dict['Wir haben für Sie gebucht'],
            )
            for row_dict in row_dicts
        ]

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name} {self.initial_value}>'

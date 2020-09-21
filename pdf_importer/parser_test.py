import unittest

from .parser import Parser


TEST_PDF = "pdf_importer/test.pdf"
HEADER_ROW_LABELS = [
    'Bu.Tag',
    'Wert',
    'Wir haben für Sie gebucht',
    'Belastung in EUR',
    'Gutschrift in EUR',
]
ROWS_DATA = [
    {
        'Bu.Tag': '02.01.',
        'Wert': '02.01.',
        # NOTE: The whitespace before the line break is expected even though
        # it's not in the PDF file because pdfminer's layout algorithm inserts
        # a whitespace between characters on the same line that don't belong
        # to the same word ('g' and '\n').
        'Wir haben für Sie gebucht': 'Dauerauftrag \nMiete vom 26.09.2019',
        'Belastung in EUR': '200,00',
    },
    {
        'Bu.Tag': '02.01.',
        'Wert': '02.01.',
        'Wir haben für Sie gebucht': (
            'Zahlungseingang \nJim Neuendorf Monatsbeitrag'
        ),
        'Gutschrift in EUR': '1.202,43',
    },
    {
        'Bu.Tag': '02.01.',
        'Wert': '03.01.',
        'Wir haben für Sie gebucht': (
            'Kartenzahlung KAUFLAND \n'
            'SVWZ+2019-12-30T15.52 21915 Debitk.0 202 \n'
            'ABWX+Kaufland//Berlin/DE'
        ),
        'Belastung in EUR': '92,06',
    },
]
WORKING_COLUMN_X_TOLERANCE = 3


class TestParser(unittest.TestCase):

    def test_default(self):
        parser = Parser(TEST_PDF)
        header_row, rows = parser.parse()

        self.assertEqual(header_row.get_texts(), HEADER_ROW_LABELS)
        # The header row's labels are 2-3 points off because
        # Apple's Numbers renders bold characters that way.
        with self.assertRaises(ValueError):
            self.assertDictEqual(rows[0].as_dict(header_row), ROWS_DATA[0])

    def test_column_x_tolerance(self):
        parser = Parser(
            TEST_PDF,
            column_x_tolerance=WORKING_COLUMN_X_TOLERANCE,
        )
        header_row, rows = parser.parse()

        self.assertEqual(header_row.get_texts(), HEADER_ROW_LABELS)
        self.assertDictEqual(rows[0].as_dict(header_row), ROWS_DATA[0])
        self.assertDictEqual(rows[1].as_dict(header_row), ROWS_DATA[1])
        self.assertDictEqual(rows[2].as_dict(header_row), ROWS_DATA[2])

    def test_max_missing_cells_per_row(self):
        parser = Parser(
            TEST_PDF,
            column_x_tolerance=WORKING_COLUMN_X_TOLERANCE,
            max_missing_cells_per_row=0,
        )
        header_row, rows = parser.parse()

        self.assertEqual(header_row.get_texts(), HEADER_ROW_LABELS)
        # There is no row that has a value for each column.
        self.assertEqual(len(rows), 0)

    def test_header_row_labels(self):
        parser = Parser(
            TEST_PDF,
            header_row_labels=HEADER_ROW_LABELS[:-1],
            column_x_tolerance=WORKING_COLUMN_X_TOLERANCE,
        )
        with self.assertRaises(ValueError) as cm:
            header_row, rows = parser.parse()
        self.assertRegex(
            cm.exception.args[0],
            r'Detected \d+ columns but',
        )

        def custom_label(old_label: str) -> str:
            return f'{old_label}1'

        custom_labels = [custom_label(label) for label in HEADER_ROW_LABELS]

        parser = Parser(
            TEST_PDF,
            header_row_labels=custom_labels,
            column_x_tolerance=WORKING_COLUMN_X_TOLERANCE,
        )
        header_row, rows = parser.parse()

        self.assertEqual(header_row.get_texts(), custom_labels)

        self.assertDictEqual(rows[0].as_dict(header_row), {
            custom_label(key): value
            for key, value in ROWS_DATA[0].items()
        })
        self.assertDictEqual(rows[1].as_dict(header_row), {
            custom_label(key): value
            for key, value in ROWS_DATA[1].items()
        })
        self.assertDictEqual(rows[2].as_dict(header_row), {
            custom_label(key): value
            for key, value in ROWS_DATA[2].items()
        })

    @unittest.skip('Not yet implemented')
    def test_alignment(self):
        pass

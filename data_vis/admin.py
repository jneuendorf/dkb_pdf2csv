from collections import defaultdict
import traceback
from io import BytesIO
from typing import DefaultDict, Iterable, List
from zipfile import ZipFile

from django.contrib import admin, messages
from django.http import FileResponse

from .models import Series, DataPoint, PdfFile
from . import utils


class DataPointInline(admin.TabularInline):
    model = DataPoint


class PdfFileInline(admin.TabularInline):
    model = PdfFile


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    inlines = [DataPointInline, PdfFileInline]
    actions = ['export_csv']

    def export_csv(self, request, queryset: Iterable[Series]):
        """See
        https://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html
        """  # NOQA
        in_memory_zip = BytesIO()
        zip = ZipFile(in_memory_zip, mode='a')

        for series in queryset:
            filename, csv_data = utils.csv_export.series_to_csv(series)
            zip.writestr(filename, csv_data)

        # fix for Linux zip files read in Windows
        for file in zip.filelist:
            file.create_system = 0

        zip.close()
        in_memory_zip.seek(0)

        return FileResponse(
            in_memory_zip,
            filename='series.zip',
            as_attachment=True,
            content_type='application/zip',
        )


@admin.register(PdfFile)
class PdfFileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'file', 'is_imported']
    actions = ['import_pdfs']

    def import_pdfs(self, request, queryset):
        if queryset.filter(series__isnull=True).count() > 0:
            raise ValueError(
                'Some of the selected PDFs do not belong to a series.'
            )

        pdfs_by_series: DefaultDict[Series, List[PdfFile]] = defaultdict(list)
        for pdf in queryset:
            pdfs_by_series[pdf.series].append(pdf)

        error_message = None
        for series, pdfs in pdfs_by_series.items():
            try:
                series.import_pdfs([pdf.file.name for pdf in pdfs], pdfs)
            except Exception as e:
                error_message = (
                    f'Error while importing PDFs for series {series.name}: '
                    f'{str(e)}'
                )
                self.message_user(request, error_message, level=messages.ERROR)
                print(error_message)
                traceback.print_exc()

        if error_message is None:
            self.message_user(
                request,
                'All PDFs were imported successfully!',
                level=messages.SUCCESS,
            )


admin.site.register(DataPoint)

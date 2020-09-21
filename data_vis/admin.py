from collections import defaultdict
from typing import DefaultDict, List

from django.contrib import admin, messages


from .models import Series, DataPoint, PdfFile


class DataPointInline(admin.TabularInline):
    model = DataPoint


class PdfFileInline(admin.TabularInline):
    model = PdfFile


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    inlines = [DataPointInline, PdfFileInline]


@admin.register(PdfFile)
class PdfFileAdmin(admin.ModelAdmin):
    readonly_fields = ['is_imported']
    actions = ["import_pdfs"]

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

        if error_message is None:
            self.message_user(
                request,
                'All PDFs were imported successfully!',
                level=messages.SUCCESS,
            )


admin.site.register(DataPoint)

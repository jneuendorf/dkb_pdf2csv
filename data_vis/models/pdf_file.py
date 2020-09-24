from django.db import models

from .validators import validate_is_pdf


class PdfFile(models.Model):
    series = models.ForeignKey(
        'Series',
        on_delete=models.CASCADE,
        related_name='pdfs',
        blank=True,
        null=True,
    )
    file = models.FileField(upload_to='pdfs/%Y/', validators=[validate_is_pdf])
    is_imported = models.BooleanField(default=False)

    def __str__(self):
        return f'<{self.__class__.__name__} {self.file.name}>'

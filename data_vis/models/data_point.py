from django.db import models


class DataPoint(models.Model):
    CSV_FIELD_NAMES = ('x', 'dy', 'meta')

    series = models.ForeignKey(
        'Series',
        on_delete=models.CASCADE,
        related_name='data_points',
    )
    x = models.DateTimeField()
    dy = models.FloatField()
    """The change in value."""
    meta = models.TextField(default='')

    class Meta:
        unique_together = ['series', 'x', 'dy', 'meta']

    def as_dict(self):
        return {
            field_name: getattr(self, field_name)
            for field_name in self.CSV_FIELD_NAMES
        }
        # return dict(x=self.x, dy=self.dy, meta=self.meta)

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.x} {self.dy} {self.meta[:10]}>'
        )

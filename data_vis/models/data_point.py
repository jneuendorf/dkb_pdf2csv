from django.db import models


def identify(x):
    return x


class DataPoint(models.Model):
    FIELD_NAMES = ('id', 'x', 'dy', 'meta', 'tags')

    series = models.ForeignKey(
        'Series',
        on_delete=models.CASCADE,
        related_name='data_points',
    )
    x = models.DateTimeField()
    dy = models.FloatField()
    """The change in value."""
    meta = models.TextField(default='')
    tags = models.ManyToManyField('Tag', related_name='data_points')

    class Meta:
        unique_together = ('series', 'x', 'dy', 'meta')

    def as_dict(self, field_names=None, **transformers):
        if field_names is None:
            field_names = self.FIELD_NAMES

        if not transformers.get('tags'):
            transformers['tags'] = lambda tags: list(
                tags.values_list('identifier', flat=True)
            )

        return {
            **{
                field_name: transformers.get(field_name, identify)(
                    getattr(self, field_name)
                )
                for field_name in field_names
            },
        }

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.x} {self.dy} {self.meta[:10]}>'
        )

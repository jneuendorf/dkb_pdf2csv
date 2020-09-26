from django.db import models


class Tag(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    meta = models.TextField(blank=True, default='')
    is_abstract = models.BooleanField(blank=True, default=False)
    """Abstract tags are not regarded when checking for untagged data points"""
    # data_points

    def __str__(self):
        return (
            f'<{self.__class__.__name__}'
            f'{" [abstract]" if self.is_abstract else ""} {self.identifier}>'
        )

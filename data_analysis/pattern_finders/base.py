from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from django.db.models import QuerySet

from data_vis.models import DataPoint


__all__ = ('Types', 'BasePatternFinder')


Subset = Iterable[DataPoint]
Subsets = Iterable[Subset]


class objectview:
    """See https://goodcode.io/articles/python-dict-object/"""

    def __init__(self, **kwargs):
        self.__dict__ = kwargs


Types = objectview(
    Subset=Subset,
    Subsets=Subsets,
    QuerySet=QuerySet,
)


class BasePatternFinder(ABC):
    data_attr = 'dy'

    @dataclass
    class Options:
        """https://stackoverflow.com/questions/51575931/"""
        min_length: int = 2
        """Specifies the minimum length that a pattern must have."""
        precision: str = 'days'
        """Specifies the granularity of time
        that points will be matched against.
        Any attribute name of relativedelta, e.g. 'days'.
        """

    def __init__(self, **options):
        self.options = self.Options(**options)

    def get_value(self, point):
        return getattr(point, self.data_attr)

    def find(self, data_points_queryset: QuerySet) -> Iterable[Subset]:
        """Finds patterns in subsets of points."""

        return [
            subset
            for subset in self.select_subsets(data_points_queryset)
            if self.should_use_subset(subset)
        ]

    @abstractmethod
    def select_subsets(self, data_points_queryset: QuerySet) -> Subsets:
        """Selects certain subsets of points to be potential patterns.
        The subsets are pattern candidates.
        """
        ...

    def should_use_subset(self, subset: Subset) -> bool:
        """Indicates if the given subset is actually a pattern.
        It acts as a filter condition for all candidates.
        """

        return bool(subset)

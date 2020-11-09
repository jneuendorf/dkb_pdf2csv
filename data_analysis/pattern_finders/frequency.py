from dataclasses import dataclass, field
import itertools
from typing import Iterable, TypedDict

from dateutil.relativedelta import relativedelta

from .base import BasePatternFinder, Types


class TimedeltaKwargs(TypedDict):
    days: int
    # seconds: int
    # microseconds: int
    # milliseconds: int
    minutes: int
    hours: int
    weeks: int


class FrequencyPatternFinder(BasePatternFinder):
    """Finds points with similar dy values and a certain frequency."""

    @dataclass
    class Options(BasePatternFinder.Options):
        intervals: Iterable[TimedeltaKwargs] = field(default_factory=list)
        """A list of timedelta kwargs that are cycled through to select
        candidates for a pattern."""
        tolerance_y: float = 0.0
        """Specifies how exact a point's dy has to match a certain value."""
        tolerance_x: TimedeltaKwargs = field(default_factory=dict)
        """Specifies how exact a point's x has to match a certain datetime"""

    def select_subsets(self,
                       data_points_queryset: Types.QuerySet) -> Types.Subsets:
        if not data_points_queryset:
            return []

        assert self.options.intervals, 'No intervals given'

        # Iterate starting points that give us (potentially) different subsets.
        # Starting points are those points lie within the interval
        # [ point0.x, point0.x + cycle_length )
        ordered_points = data_points_queryset.order_by('x')
        first_point = ordered_points.first()
        starting_time = first_point.x

        deltas = [
            relativedelta(**interval)
            for interval in self.options.intervals
        ]
        abstract_cycle_length = sum(deltas, relativedelta())
        # Note: Without applying the delta to a datetime the number of e.g.
        # days can't be determined because months have different amounts of
        # days, i.e. relativedelta(months=1).days == 0.
        # But when the delta is added to a concrete datetime, the number of
        # days becomes clear, e.g.
        # (
        #   date(2020,2,1) + relativedelta(months=2) - date(2020,2,1)
        # ).days == 60
        # because the February 2020 has 29 days.
        applied_cycle_length = (
            (starting_time + abstract_cycle_length)
            - starting_time
        )
        num_atomic_periods = getattr(
            applied_cycle_length,
            self.options.precision,
        )
        atomic_delta = relativedelta(**{self.options.precision: 1})
        subsets = []

        tolerance_x = relativedelta(**self.options.tolerance_x)

        for i in range(num_atomic_periods):
            delta_iterator = itertools.cycle(deltas)
            subset = {}
            time_cursor = starting_time + (i * atomic_delta)

            while True:
                points_at_x = data_points_queryset.filter(
                    x__gte=time_cursor - tolerance_x,
                    x__lte=time_cursor + tolerance_x,
                )
                if points_at_x:
                    subset[time_cursor] = list(points_at_x)
                if not data_points_queryset.filter(x__gte=time_cursor):
                    break
                time_cursor += next(delta_iterator)

            # We must not use empty subsets because the cartesian product with
            # any empty set returns an empty set:
            #   itertools.product([1, 2], []) == []
            if subset:
                subsets.append(subset)

        # At this point, a subset can contain multiple points with the same
        # datetime. But we don't want to have patterns like that.
        # For example let's say we have a weekly frequency:
        # date ||     01-01   ||  01-08  ||  01-15
        # i    || 0   | 1 | 2 || 3   | 4 || 5   | 6
        # dy   || 100 | ? | ? || 100 | ? || 100 | 100
        # Right now, the points at i=[0, 3, 5, 6] would form a subset.
        # We want exactly 1 point per datetime, which means we will get
        # multiple subsets instead:
        # [0, 3, 5] and [0, 3, 6]
        # Therefore, we create the cartesian product of points for all
        # datetimes, which gives us all the lines we could draw that only hit
        # one point per datetime:
        #   list(itertools.product([1,2,3], [4,5], [6,7]))
        #   [
        #       (1, 4, 6), (1, 4, 7), (1, 5, 6), (1, 5, 7),
        #       (2, 4, 6), (2, 4, 7), (2, 5, 6), (2, 5, 7),
        #       (3, 4, 6), (3, 4, 7), (3, 5, 6), (3, 5, 7)
        #   ]
        result = itertools.chain.from_iterable(
            itertools.product(*subset.values()) for subset in subsets
        )

        min_length = self.options.min_length
        return (
            pattern
            for pattern in result
            if len(pattern) >= min_length
        )

    def should_use_subset(self, subset: Types.Subset) -> bool:
        if not super().should_use_subset(subset):
            return False

        tolerance = self.options.tolerance_y
        # TODO: Maybe add an option for only having e.g. 90% of the points
        #   fulfill the tolerance condition
        return all(
            abs(p.dy - q.dy) <= tolerance
            for p, q in itertools.combinations(subset, 2)
        )

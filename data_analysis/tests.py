from datetime import datetime, timezone
# from itertools import zip_longest
from pprint import pprint
import unittest

from django.db.models import Model
from django.test import TestCase
from iterable_orm import QuerySet

from data_analysis.pattern_finders.frequency import FrequencyPatternFinder
from data_vis.models import Series, DataPoint


# from data_analysis.test import *

def utc_dt(*args, **kwargs):
    return datetime(*args, **kwargs, tzinfo=timezone.utc)


data_points = QuerySet([
    DataPoint(x=utc_dt(2020, 1, 1), dy=100),
    DataPoint(x=utc_dt(2020, 1, 1), dy=-100),
    DataPoint(x=utc_dt(2020, 1, 4), dy=2),
    DataPoint(x=utc_dt(2020, 2, 1), dy=95),
    DataPoint(x=utc_dt(2020, 2, 5), dy=200),
    # DataPoint(x=utc_dt(2020, 3, 1), dy=105),
    DataPoint(x=utc_dt(2020, 4, 4), dy=-4),
])


# TODO: make real tests
def f():
    series = Series.objects.first()
    finder = FrequencyPatternFinder(intervals=[dict(weeks=1)])
    subsets = finder.find(series.data_points.filter(x__lte='2020-04-01'))
    pprint(subsets)


def g():
    finder = FrequencyPatternFinder(
        intervals=[dict(months=1)],
        tolerance_y=10,
    )
    # series = Series.objects.first()
    # patterns = finder.find(series.data_points.filter(x__lte='2020-03-01'))
    patterns = finder.find(data_points)
    pprint(patterns)


# def assert_model_equal(self, m1, m2, msg=None, field_names=None):
#     """https://stackoverflow.com/a/38258448/6928824"""
#
#     self.assertTrue(
#         isinstance(m1, Model) and isinstance(m2, Model),
#         'One of the arguments is no model instance',
#     )
#     self.assertTrue(
#         m1._meta.concrete_model == m2._meta.concrete_model,
#         'The arguments meta concrete models do not match',
#     )
#     if m1 is m2:
#         return
#
#     meta = m1._meta
#     if field_names is None:
#         fields = meta.get_fields()
#     else:
#         fields = [meta.get_field(field_name) for field_name in field_names]
#
#     import pudb; pudb.set_trace()
#
#     for field in fields:
#         if field.name != meta.pk.attname:
#             self.assertEqual(
#                 getattr(m1, field.name),
#                 getattr(m2, field.name),
#                 f'Model instances have different values for {field.name}',
#             )
#             # self.failureException(msg)


# def bound_assert(f, self, **kwargs):
#     def assert_equal(a, b, msg=None):
#         return f(self, a, b, msg, **kwargs)
#     return assert_equal


class TestFrequencyPatternFinder(TestCase):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.addTypeEqualityFunc(
    #         DataPoint,
    #         bound_assert(assert_model_equal, self, field_names=('x', 'dy')),
    #     )

    def setUp(self):
        simple = Series.objects.create(name='simple')
        simple.data_points.bulk_create([
            DataPoint(series=simple, x=utc_dt(2020, 1, 1), dy=100),
            DataPoint(series=simple, x=utc_dt(2020, 1, 1), dy=-100),
            DataPoint(series=simple, x=utc_dt(2020, 1, 4), dy=2),
            DataPoint(series=simple, x=utc_dt(2020, 2, 1), dy=95),
            DataPoint(series=simple, x=utc_dt(2020, 2, 5), dy=200),
            # DataPoint(series=simple, x=utc_dt(2020, 3, 1), dy=105),
            DataPoint(series=simple, x=utc_dt(2020, 4, 4), dy=-4),
        ])

        unaligned = Series.objects.create(name='unaligned')
        unaligned.data_points.bulk_create([
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=-118.0),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=-29.05),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=-21.82),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=-14.51),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=-11.36),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=-9.43),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=601.82),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 4), dy=1202.43),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 5), dy=-149.57),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 5), dy=-48.82),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 5), dy=-25.0),
            DataPoint(series=unaligned, x=utc_dt(2020, 5, 5), dy=50.0),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 1), dy=-118.0),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 1), dy=601.82),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 1), dy=1202.43),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 2), dy=-134.99),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 2), dy=-29.91),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 2), dy=-29.05),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 2), dy=-21.82),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 2), dy=-14.51),
            DataPoint(series=unaligned, x=utc_dt(2020, 6, 2), dy=-11.36),
        ])

    # def assertModelsEqual(self, m1, m2, *, field_names=None):
    #     """https://stackoverflow.com/a/38258448/6928824"""
    #
    #     self.assertTrue(
    #         isinstance(m1, Model) and isinstance(m2, Model),
    #         'One of the arguments is no model instance',
    #     )
    #     self.assertTrue(
    #         m1._meta.concrete_model == m2._meta.concrete_model,
    #         'The arguments meta concrete models do not match',
    #     )
    #     if m1 is m2:
    #         return
    #
    #     meta = m1._meta
    #     if field_names is None:
    #         fields = meta.get_fields()
    #     else:
    #         fields = [meta.get_field(field_name) for field_name in field_names]
    #
    #     for field in fields:
    #         if field.name != meta.pk.attname:
    #             self.assertEqual(
    #                 getattr(m1, field.name),
    #                 getattr(m2, field.name),
    #                 f'Model instances have different values for {field.name}',
    #             )
    #
    # def assertModelIterablesEqual(self, l1, l2, **kwargs):
    #     print('assertModelIterablesEqual')
    #     pprint(l1)
    #     pprint(l2)
    #     for m1, m2 in zip_longest(l1, l2):
    #         self.assertModelsEqual(m1, m2, **kwargs)
    #
    # def assertPatternsEqual(self, p1, p2, **kwargs):
    #     for pattern_tuples in zip_longest(p1, p2, fillvalue=()):
    #         self.assertModelIterablesEqual(*pattern_tuples, **kwargs)

    # @unittest.skip("---------")
    def test_simple_data(self):
        finder = FrequencyPatternFinder(
            intervals=[dict(months=1)],
            tolerance_y=10,
        )
        patterns = finder.find(
            Series.objects.get(name='simple').data_points.all()
        )

        self.assertEqual(
            patterns,
            {
                (
                    DataPoint.objects.get(x=utc_dt(2020, 1, 1), dy=100),
                    DataPoint.objects.get(x=utc_dt(2020, 2, 1), dy=95),
                ),
                (
                    DataPoint.objects.get(x=utc_dt(2020, 1, 4), dy=2),
                    DataPoint.objects.get(x=utc_dt(2020, 4, 4), dy=-4),
                ),
            },
        )

    # @unittest.skip("---------")
    def test_data_with_unaligned_peaks(self):
        finder = FrequencyPatternFinder(
            intervals=[dict(months=1)],
            tolerance_y=0,
            tolerance_x=dict(days=3),
        )
        patterns = finder.find(
            Series.objects.get(name='unaligned').data_points.all()
        )

        self.assertEqual(
            patterns,
            {
                (
                    DataPoint.objects.get(x=utc_dt(2020, 5, 4), dy=-118.0),
                    DataPoint.objects.get(x=utc_dt(2020, 6, 1), dy=-118.0),
                ),
                (
                    DataPoint.objects.get(x=utc_dt(2020, 5, 4), dy=-29.05),
                    DataPoint.objects.get(x=utc_dt(2020, 6, 2), dy=-29.05),
                ),
                (
                    DataPoint.objects.get(x=utc_dt(2020, 5, 4), dy=-21.82),
                    DataPoint.objects.get(x=utc_dt(2020, 6, 2), dy=-21.82)
                ),
                (
                    DataPoint.objects.get(x=utc_dt(2020, 5, 4), dy=-14.51),
                    DataPoint.objects.get(x=utc_dt(2020, 6, 2), dy=-14.51),
                ),
                (
                    DataPoint.objects.get(x=utc_dt(2020, 5, 4), dy=-11.36),
                    DataPoint.objects.get(x=utc_dt(2020, 6, 2), dy=-11.36),
                ),
                (
                    DataPoint.objects.get(x=utc_dt(2020, 5, 4), dy=601.82),
                    DataPoint.objects.get(x=utc_dt(2020, 6, 1), dy=601.82),
                ),
                (
                    DataPoint.objects.get(x=utc_dt(2020, 5, 4), dy=1202.43),
                    DataPoint.objects.get(x=utc_dt(2020, 6, 1), dy=1202.43),
                ),
                # # duplicate
                # (
                #     DataPoint(x=utc_dt(2020, 5, 4), dy=-29.05),
                #     DataPoint(x=utc_dt(2020, 6, 2), dy=-29.05),
                # ),
                # # duplicate
                # (
                #     DataPoint(x=utc_dt(2020, 5, 4), dy=-21.82),
                #     DataPoint(x=utc_dt(2020, 6, 2), dy=-21.82),
                # ),
                # # duplicate
                # (
                #     DataPoint(x=utc_dt(2020, 5, 4), dy=-14.51),
                #     DataPoint(x=utc_dt(2020, 6, 2), dy=-14.51),
                # ),
                # # duplicate
                # (
                #     DataPoint(x=utc_dt(2020, 5, 4), dy=-11.36),
                #     DataPoint(x=utc_dt(2020, 6, 2), dy=-11.36),
                # ),
            },
            # field_names=('x', 'dy'),
        )

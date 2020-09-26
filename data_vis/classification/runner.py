from django.db.models import Count

from data_vis.models import DataPoint, Tag

from .classifiers import ALL


def run(untagged_only=False, dry_run=False):
    tags = Tag.objects.all()
    if untagged_only:
        DataPoint.objects.annotate(num_tags=Count('tags')).filter(num_tags=0)
    else:
        data_points = DataPoint.objects.all()

    classifiers = [Classifier(tags) for Classifier in ALL]

    for point in data_points:
        tags_for_point = set()
        for classifier in classifiers:
            tags_for_point |= set(classifier.run(point))

        if dry_run:
            print(point.id)
            print(point.meta)
            print(tags_for_point)
            print()
        else:
            point.tags.set(tags_for_point)

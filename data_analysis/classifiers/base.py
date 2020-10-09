from abc import ABC, abstractmethod


class BaseClassifier(ABC):
    EXPORTABLES = ()

    tag_queryset = None
    tag_meta_vars = None

    def __init__(self, tag_queryset):
        self.tag_queryset = tag_queryset
        self.tag_meta_vars = self.get_tag_meta_vars(tag_queryset)

    def run(self, data_point):
        """Injects instances attributes into the 'classify' method
        in order to provide a easier and functional interface for that method.
        """

        return self.classify(
            data_point,
            self.tag_queryset,
            self.tag_meta_vars,
        )

    @abstractmethod
    def classify(self, data_point, tag_queryset, tag_meta_vars) -> list:
        """Classifies the given data point as zero, one or multiple
        of the given existing tag_queryset.

        Parameters:
        - data_point: data_vis.models.DataPoint
        - tag_queryset: Iterable[data_vis.models.Tag]
        - tag_meta_vars: Dict[str, Dict[str, Any]]
            Maps tag.identifier to tag.meta intpreted as python code

        Returns: List[dava_vis.models.Tag]
        """
        pass

    def get_tag_meta_vars(self, tag_queryset):
        tag_meta_vars = {}
        exportable_vars = self.EXPORTABLES
        errors = {}

        for tag in tag_queryset:
            locals = {}

            try:
                exec(tag.meta, globals(), locals)
            except SyntaxError as e:
                errors[tag.identifier] = e
                continue

            tag_meta_vars[tag.identifier] = {
                exportable_var: locals.get(exportable_var)
                for exportable_var in exportable_vars
            }

        if errors:
            raise ValueError(errors)

        return tag_meta_vars

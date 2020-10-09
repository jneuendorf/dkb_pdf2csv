from .base import BaseClassifier


class KeywordClassifier(BaseClassifier):
    EXPORTABLES = (
        'KEYWORDS',
        'PATTERNS',
    )

    def classify(self, data_point, tag_queryset, tag_meta_vars):
        meta = data_point.meta.lower()
        matched_identifiers = [
            identifier
            for identifier, vars in tag_meta_vars.items()
            if any(
                (keyword.lower() in meta)
                for keyword in vars['KEYWORDS'])
        ]
        return tag_queryset.filter(identifier__in=matched_identifiers)

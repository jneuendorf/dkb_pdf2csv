from django.core.serializers.json import DjangoJSONEncoder


class JsonEncoder(DjangoJSONEncoder):
    """Additional types: set, tuple"""

    def default(self, obj):
        if isinstance(obj, (set, tuple)):
            return list(obj)
        return super().default(obj)

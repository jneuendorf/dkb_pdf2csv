from django.core.serializers.json import DjangoJSONEncoder


class JsonEncoder(DjangoJSONEncoder):
    """Additional types: set, tuple"""

    def default(self, obj):
        if isinstance(obj, (set, tuple)):
            return list(obj)
        # if hasattr(obj, 'to_json') and callable(obj.to_json):
        #     return obj.to_json()
        return super().default(obj)

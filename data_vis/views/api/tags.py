from django.http import HttpRequest, JsonResponse

from ...models import Tag
from .serializers import JsonEncoder


def tags(request: HttpRequest):
    return JsonResponse(
        list(Tag.objects.values('identifier', 'is_abstract')),
        encoder=JsonEncoder,
        safe=False,
    )

from django.shortcuts import render
from django.http import HttpRequest


def test(request: HttpRequest):
    return render(request, 'data_vis/test.html', {})

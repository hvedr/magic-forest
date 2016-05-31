from django.shortcuts import render
import json
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, "index.html")


def generate(request):
    response = {
        "url": "/static/img/rendered/example.jpg"
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request, "beans/index.html", {})


def magic(request):
    query = request.POST.get("query")
    return JsonResponse({'foo' : 'bar'})

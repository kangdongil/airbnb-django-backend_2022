from django.core import serializers
from django.http import HttpResponse
from .models import Category

def categories(request):
    all_categories = Category.objects.all()
    data = serializers.serialize("json", all_categories)
    return HttpResponse(content=data)

def category(request, pk):
    category = Category.objects.get(pk=pk)
    data = serializers.serialize("json", [category])
    return HttpResponse(content=data)
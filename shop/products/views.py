from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('index')


def product(request, product_id):
    return HttpResponse('product' + product_id)

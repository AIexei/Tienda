from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.


def index(request):
    context = {}
    context['skus'] = SKU.objects.all()

    return render(request, 'index.html', context)


def product(request, sku_id):
    sku = SKU.objects.get(id=sku_id)

    context = {}
    context['sku'] = sku
    context['product'] = sku.product

    return render(request, 'product.html', context)


# login required
def favourites(request):
    return HttpResponse('favourites')
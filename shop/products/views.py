from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.


def index(request):
    context = dict()
    context['skus'] = SKU.objects.all()
    context['can_search'] = True

    return render(request, 'index.html', context)


def product(request, sku_id):
    sku = SKU.objects.get(id=sku_id)

    context = dict()
    context['sku'] = sku
    context['product'] = sku.product
    context['can_search'] = True

    return render(request, 'product.html', context)


def search(request):
    context = dict()
    context['can_search'] = True

    return render(request, 'search.html', context)


# login required
def favourites(request):
    context = dict()
    context['can_search'] = True

    return render(request, 'favourites.html', context)
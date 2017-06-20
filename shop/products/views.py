from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from .models import *


# Create your views here.


def index(request):
    context = dict()
    context['skus'] = SKU.objects.all()
    context['nodes'] = Category.objects.all()
    context['can_search'] = True

    return render(request, 'index.html', context)


def product(request, sku_id):
    sku = SKU.objects.get(id=sku_id)

    context = dict()
    context['sku'] = sku
    context['product'] = sku.product
    context['can_search'] = True
    context['comments'] = sku.comments.all()

    return render(request, 'product.html', context)


def search(request):
    # SKU.objects.filter(product__manufacturer__name='Xiaomi', color='gy', product__in=Category.objects.get(name='Phones').products.all())

    if request.is_ajax():
        queryset = SKU.objects.filter(product__in=Category.objects.get(name=request.GET['cname']).products.all())
        html = render_to_string('search-div.html', {'skus': queryset})
        return HttpResponse(html)

    context = dict()
    context['can_search'] = True
    context['categories'] = Category.objects.all().order_by('level')
    context['manufacturers'] = Manufacturer.objects.all().order_by('name')
    context['colors'] = sorted([x[1] for x in SKU.COLOR_CHOICES])
    context['skus'] = SKU.objects.all()

    return render(request, 'search.html', context)


# login required
def favourites(request):
    user_profile = UserProfile.objects.get(user__id=request.user.id)

    context = dict()
    context['can_search'] = True
    context['liked_skus'] = user_profile.favourites.all()
    context['is_empty'] = not bool(context['liked_skus'].count())

    return render(request, 'favourites.html', context)
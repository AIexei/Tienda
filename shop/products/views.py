from django.shortcuts import render, HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.template .context_processors import csrf
from django.db.models import QuerySet
from .models import *
import json


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
    context.update(csrf(request))
    context['sku'] = sku
    context['product'] = sku.product
    context['can_search'] = True
    context['comments'] = sku.comments.all()

    try:
        user_profile = UserProfile.objects.get(user__id=request.user.id)
        context['is_liked'] = bool(user_profile.favourites.filter(id=sku.id))
    except Exception as e:
        print(e)

    return render(request, 'product.html', context)


def search(request):
    queryset = SKU.objects.all()

    try:
        if 'cat' in request.GET:
            category = request.GET['cat']
            queryset = queryset.filter(product__in=Category.objects.get(name=category).products.all())

        if 'clrs' in request.GET:
            colors = json.loads(request.GET['clrs'])
            queryset = queryset.filter(color__in=colors)

        if 'manufs' in request.GET:
            manufacturers = json.loads(request.GET['manufs'])
            queryset = queryset.filter(product__manufacturer__name__in=manufacturers)

    except Exception:
        queryset = SKU.objects.none()


    if request.is_ajax():
        html = render_to_string('includes/search-div.html', {'skus': queryset})
        return HttpResponse(html)

    context = dict()
    context['can_search'] = True
    context['categories'] = Category.objects.all().order_by('level')
    context['manufacturers'] = Manufacturer.objects.all().order_by('name')
    context['colors'] = sorted([x[1] for x in SKU.COLOR_CHOICES])
    context['skus'] = queryset

    return render(request, 'search.html', context)


@login_required
def favourites(request):
    user_profile = UserProfile.objects.get(user__id=request.user.id)

    context = dict()
    context['can_search'] = True
    context['liked_skus'] = user_profile.favourites.all()
    context['is_empty'] = not bool(context['liked_skus'].count())

    return render(request, 'favourites.html', context)


@login_required
def like_action(request):
    sku_id = int(request.GET['id'])
    sku = SKU.objects.get(id=sku_id)

    user_profile = UserProfile.objects.get(user__id=request.user.id)
    action = request.GET['action']

    if action == 'lk':
        user_profile.favourites.add(sku)
        data = {'is_liked': True}
    else:
        user_profile.favourites.remove(sku)
        data = {'is_liked': False}

    user_profile.save()
    html = render_to_string('includes/btns.html', data)

    return HttpResponse(html)


@login_required
def add_comment(request):
    if request.POST:
        pass
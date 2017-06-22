from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.template .context_processors import csrf
from django.views.generic import ListView
from ratelimit.decorators import ratelimit
from .models import *
import json

'''
class Index(ListView):
    model = SKU
    template_name = 'index.html'
    context_object_name = 'skus'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['nodes'] = Category.objects.all()
        context['can_search'] = True
        return context
'''


def index(request):
    context = dict()

    sku_related_field = ['product__name', 'product__manufacturer__name']
    context['skus'] = SKU.objects.select_related().only(*sku_related_field)
    context['nodes'] = Category.objects.all()
    context['can_search'] = True

    return render(request, 'products/index.html', context)


def product(request, sku_id):
    sku = SKU.objects.get(id=sku_id)

    context = dict()
    context.update(csrf(request))
    context['sku'] = sku
    context['product'] = sku.product
    context['can_search'] = True

    comment_related_field = ['owner__user__username']
    context['comments'] = sku.comments.select_related().only(*comment_related_field).order_by('-time')

    try:
        user_profile = UserProfile.objects.get(user__id=request.user.id)
        context['is_liked'] = bool(user_profile.favourites.filter(id=sku.id))
    except Exception as e:
        print(e)

    return render(request, 'products/product.html', context)


@ratelimit(key='ip', rate='5/s', block=True)
def search(request):
    sku_related_fields = ['product__name', 'product__manufacturer__name']
    defer_fields = ['screen_diagonal', 'screen_resolution', 'body_maretial', 'weight', 'battery_capacity']
    queryset = SKU.objects.defer(*defer_fields).select_related().only(*sku_related_fields)

    try:
        if 'cat' in request.GET:
            category = request.GET['cat']
            queryset = queryset.filter(product__in=Category.objects.get(name=category).products.only('id'))

        if 'clrs' in request.GET:
            colors = json.loads(request.GET['clrs'])
            queryset = queryset.filter(color__in=colors)

        if 'manufs' in request.GET:
            manufacturers = json.loads(request.GET['manufs'])
            queryset = queryset.filter(product__manufacturer__name__in=manufacturers)

        if 'has_wifi' in request.GET:
            if request.GET['has_wifi']:
                queryset = queryset.filter(product__has_wifi=True)

        if 'has_bluetooth' in request.GET:
            if request.GET['has_bluetooth']:
                queryset = queryset.filter(product__has_bluetooth=True)

    except Exception:
        queryset = SKU.objects.none()


    if request.is_ajax():
        data = {'skus': queryset, 'is_empty': not bool(queryset.count())}
        html = render_to_string('products/includes/search-div.html', data)
        return HttpResponse(html)

    context = dict()
    context['can_search'] = True
    context['categories'] = Category.objects.only('name').order_by('level')
    context['manufacturers'] = Manufacturer.objects.only('name').order_by('name')
    context['colors'] = sorted([x[1] for x in SKU.COLOR_CHOICES])
    context['is_empty'] = not bool(queryset.count())
    context['skus'] = queryset

    return render(request, 'products/search.html', context)


@login_required
def favourites(request):
    user_profile = UserProfile.objects.get(user__id=request.user.id)
    sku_related_fields = ['product__name', 'product__manufacturer__name']

    context = dict()
    context['can_search'] = True
    context['liked_skus'] = user_profile.favourites.select_related().only(*sku_related_fields)
    context['is_empty'] = not bool(context['liked_skus'].count())

    return render(request, 'products/favourites.html', context)


@login_required
def like_action(request):
    sku_id = int(request.GET['id'])
    user_profile = UserProfile.objects.get(user__id=request.user.id)
    action = request.GET['action']

    if action == 'lk':
        user_profile.favourites.add(sku_id)
        data = {'is_liked': True}
    else:
        user_profile.favourites.remove(sku_id)
        data = {'is_liked': False}

    user_profile.save()
    html = render_to_string('products/includes/btns.html', data)

    return HttpResponse(html)


@login_required
@ratelimit(key='user', rate='5/m', block=True)
def add_comment(request, sku_id):
    if request.POST and request.is_ajax():
        text = request.POST['content']
        user_profile = UserProfile.objects.only('id').get(user__id=request.user.id)
        sku = SKU.objects.get(id=sku_id)

        sku.comments.create(owner=user_profile, content=text)

        comment_related_field = ['owner__user__username']
        data = {'comments': sku.comments.select_related().only(*comment_related_field).order_by('-time')}

        html = render_to_string('products/includes/comments.html', data)
        return HttpResponse(html)
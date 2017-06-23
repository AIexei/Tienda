from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template .context_processors import csrf
from django.views.generic import ListView, DetailView
from ratelimit.decorators import ratelimit
from .models import *
import json


class IndexView(ListView):
    model = SKU
    context_object_name = 'skus'
    template_name = 'products/index.html'


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['nodes'] = Category.objects.all()
        context['can_search'] = True
        return context


    def get_queryset(self):
        only_fields = ['product__name', 'product__manufacturer__name']
        queryset = self.model.objects.select_related().only(*only_fields)
        return queryset


class FavouritesView(ListView):
    model = SKU
    context_object_name = 'liked_skus'
    template_name = 'products/favourites.html'


    def get_context_data(self, **kwargs):
        context = super(FavouritesView, self).get_context_data(**kwargs)
        context['can_search'] = True
        context['is_empty'] = not bool(context[self.context_object_name].count())
        return context


    def get_queryset(self):
        user_profile = UserProfile.objects.get(user__id=self.request.user.id)

        only_fields = ['product__name', 'product__manufacturer__name']
        queryset = user_profile.favourites.select_related().only(*only_fields)
        return queryset


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FavouritesView, self).dispatch(request, *args, **kwargs)


class SearchView(ListView):
    model = SKU
    context_object_name = 'skus'
    template_name = 'products/search.html'


    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object_list = self.get_queryset()
            context = self.get_context_data_for_ajax()
            html = render_to_string('products/includes/search-div.html', context)
            return HttpResponse(html)

        return super(SearchView, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['can_search'] = True
        context['categories'] = Category.objects.only('name').order_by('level')
        context['manufacturers'] = Manufacturer.objects.only('name').order_by('name')
        context['is_empty'] = not bool(context[self.context_object_name].count())
        context['colors'] = sorted([x[1] for x in SKU.COLOR_CHOICES])
        return context


    def get_context_data_for_ajax(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['is_empty'] = not bool(context[self.context_object_name].count())
        return context


    def get_queryset(self):
        only_fields = ['product__name', 'product__manufacturer__name']
        queryset = self.model.objects.select_related().only(*only_fields)

        try:
            if 'cat' in self.request.GET:
                category = self.request.GET['cat']
                queryset = queryset.filter(product__in=Category.objects.get(name=category).products.only('id'))

            if 'clrs' in self.request.GET:
                colors = json.loads(self.request.GET['clrs'])
                queryset = queryset.filter(color__in=colors)

            if 'manufs' in self.request.GET:
                manufacturers = json.loads(self.request.GET['manufs'])
                queryset = queryset.filter(product__manufacturer__name__in=manufacturers)

            if 'has_wifi' in self.request.GET:
                if self.request.GET['has_wifi']:
                    queryset = queryset.filter(product__has_wifi=True)

            if 'has_bluetooth' in self.request.GET:
                if self.request.GET['has_bluetooth']:
                    queryset = queryset.filter(product__has_bluetooth=True)
        except:
            queryset = self.model.objects.none()

        return queryset


    @method_decorator(ratelimit(key='ip', rate='5/s', block=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SearchView, self).dispatch(request, *args, **kwargs)


class ProductView(DetailView):
    model = SKU
    context_object_name = 'sku'
    template_name = 'products/product.html'


    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['can_search'] = True
        context['product'] = self.object.product
        context['comments'] = self.object.comments.select_related().only('owner__user__username').order_by('-time')
        context['is_liked'] = self.is_liked_product()
        return context


    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            sku_id = self.kwargs['sku_id']
            obj = queryset.get(id=sku_id)
        except:
            raise Http404()

        return obj


    def is_liked_product(self):
        try:
            user_profile = UserProfile.objects.get(user__id=self.request.user.id)
            return bool(user_profile.favourites.filter(id=self.kwargs['sku_id']))
        except:
            return False



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
from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.template .context_processors import csrf
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from ratelimit.decorators import ratelimit
from .models import *
import json


class IndexView(ListView):
    model = SKU
    context_object_name = 'skus'
    template_name = 'products/index.html'
    paginate_by = 8


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['nodes'] = Category.objects.all()
        context['can_search'] = True
        return context


    def get_queryset(self):
        only_fields = ['product__name', 'product__manufacturer__name', 'batch',]
        queryset = self.model.objects.select_related().only(*only_fields).order_by('-batch__count', '-likes')
        return queryset


class FavouritesView(LoginRequiredMixin, ListView):
    model = SKU
    context_object_name = 'liked_skus'
    template_name = 'products/favourites.html'
    paginate_by = 12


    def get_context_data(self, **kwargs):
        context = super(FavouritesView, self).get_context_data(**kwargs)
        context['can_search'] = True
        context['is_empty'] = not bool(context[self.context_object_name].count())
        return context


    def get_queryset(self):
        user_profile = UserProfile.objects.get(user__id=self.request.user.id)

        only_fields = ['product__name', 'product__manufacturer__name', 'batch',]
        queryset = user_profile.favourites.select_related().only(*only_fields)
        return queryset


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
        context['expr'] = self.get_expr()
        return context


    def get_context_data_for_ajax(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['is_empty'] = not bool(context[self.context_object_name].count())
        context['expr'] = self.get_expr()
        return context


    def get_queryset(self):
        only_fields = ['product__name', 'product__manufacturer__name', 'batch',]
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

            if 'expr' in self.request.GET:
                string = self.get_expr()
                strings = string.split(' ')

                skus = list(queryset)

                for s in strings:
                    skus = list(filter(lambda x: re.search(s, x.product.manufacturer.name +
                                                           ' ' + x.product.name, re.IGNORECASE), skus))

                ids = map(lambda x: x.id, skus)
                queryset = SKU.objects.filter(id__in=ids)
        except:
            queryset = self.model.objects.none()

        return queryset.order_by('-batch__count', '-likes')


    def get_expr(self):
        return self.request.GET.get('expr', None)


    @method_decorator(ratelimit(key='ip', rate='5/s', block=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SearchView, self).dispatch(request, *args, **kwargs)


class ProductView(DetailView):
    model = SKU
    context_object_name = 'sku'
    template_name = 'products/product.html'


    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['can_search'] = False
        context['product'] = self.object.product
        context['comments'] = self.object.comments.select_related().only('owner__user__username').order_by('-time')
        context['is_liked'] = self.is_liked_product()
        context['batch'] = self.object.batch
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


class LikeUpdate(LoginRequiredMixin, UpdateView):
    http_method_names = ['get']
    template_name = 'products/includes/btns.html'


    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            sku_id = int(request.GET['id'])
            sku = SKU.objects.get(id=sku_id)

            action = request.GET['action']
            status = self.get_action_status(action, sku_id)
            batch = sku.batch
            product = sku.product

            context = {'is_liked': status, 'batch': batch, 'product': product}
            html = render_to_string(self.template_name, context)
            return HttpResponse(html)

        raise Http404()


    def get_action_status(self, action, sku_id):
        user_profile = UserProfile.objects.get(user__id=self.request.user.id)
        sku = SKU.objects.get(id=sku_id)
        result = True

        if action == 'lk':
            sku.likes = sku.likes + 1
            user_profile.favourites.add(sku_id)
        else:
            sku.likes = sku.likes - 1
            user_profile.favourites.remove(sku_id)
            result = False

        sku.save()
        user_profile.save()
        return result


    def http_method_not_allowed(self, request, *args, **kwargs):
        raise Http404()


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    context_object_name = 'comments'
    http_method_names = ['post']
    template_name = 'products/includes/comments.html'
    fields = ['content']


    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            text = request.POST['content']
            sku_id = int(self.kwargs['sku_id'])

            self.create_comment(text, sku_id)

            html = render_to_string(self.template_name, self.get_context_data())
            return HttpResponse(html)

        raise Http404()


    def create_comment(self, text, sku_id):
        user_profile = UserProfile.objects.only('id').get(user__id=self.request.user.id)
        self.sku = SKU.objects.get(id=sku_id)
        self.sku.comments.create(owner=user_profile, content=text)


    def get_context_data(self, **kwargs):
        context ={self.context_object_name: self.get_queryset()}
        return context


    def get_queryset(self):
        only_fields = ['owner__user__username']
        queryset = self.sku.comments.select_related().only(*only_fields).order_by('-time')
        return queryset


    def http_method_not_allowed(self, request, *args, **kwargs):
        raise Http404()


    @method_decorator(ratelimit(key='user', rate='5/m', block=True))
    def dispatch(self, request, *args, **kwargs):
        return super(CommentCreate, self).dispatch(request, *args, **kwargs)


class Payment(LoginRequiredMixin, View):
    http_method_names = ['post',]

    # UPDATE
    def post(self, request, *args, **kwargs):
        prev_cost = int(self.kwargs['cost'])
        sku_id = self.kwargs['sku_id']
        batch = SKU.objects.get(id=sku_id).batch

        if batch.count == 0:
            print('no products')
        elif prev_cost != batch.cost:
            print('product cost changed')
        else:
            batch.count = batch.count - 1
            batch.save()

        redirect_url = '/product/id' + sku_id
        return redirect(redirect_url)


    def http_method_not_allowed(self, request, *args, **kwargs):
        raise Http404()
from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    context = {}



    return render(request, 'index.html', context)


def product(request, product_id):
    return HttpResponse('product' + product_id)


# login required
def favourites(request):
    return HttpResponse('favourites')
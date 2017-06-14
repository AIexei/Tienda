from django.shortcuts import render, HttpResponse

# Create your views here.


def user_login(request):
    return HttpResponse('login')


def user_logout(request):
    return HttpResponse('logout')


def user_register(request):
    return HttpResponse('register')
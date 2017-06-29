from django.shortcuts import render, redirect
from django.views.generic import RedirectView, FormView, View
from django.contrib.auth import login, logout, authenticate
from .forms import UserForm
from .models import User, UserProfile
import re


class RegisterView(FormView):
    url = '/auth/register/'
    success_url = '/'
    form_class = UserForm
    template_name = 'loginsys/register.html'


    def get_context_data(self, **kwargs):
        context = {
            'register_form': UserForm(),
            'message': kwargs.get('message')
        }

        return context


    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        if User.objects.filter(username=email).exists():
           return self.error('User with email exists.')

        if password != confirm_password:
            return self.error('Passwords don\'t match.')

        if not self.valid_password(password):
            return self.error('Invalid password.')

        instance = form.save(commit=False)
        instance.username = email
        instance.set_password(password)
        instance.save()

        UserProfile.objects.create(user=instance)
        login(self.request, instance)
        return redirect(self.success_url)


    def valid_password(self, password):
        return bool(re.match(r'^[\d|a-zA-z]{8,}$', password))


    def error(self, msg):
        context = self.get_context_data(message=msg)
        return render(self.request, self.template_name, context)


    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return redirect(self.success_url)

        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class LoginView(View):
    success_url = '/'
    url = '/auth/login/'
    template_name = 'loginsys/login.html'


    def get(self, request, context=None):
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(self.success_url)
            else:
                context = {'message': 'Your account is deactivated.'}
                return self.get(request, context)
        else:
            context = {'message': 'Invalid data.'}
            return self.get(request, context)


    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return redirect(self.success_url)

        return super(LoginView, self).dispatch(request, *args, **kwargs)


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
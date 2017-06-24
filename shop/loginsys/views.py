from django.shortcuts import render, redirect
from django.views.generic import RedirectView, FormView, View
from django.contrib.auth import login, logout, authenticate
from .forms import UserForm

'''
class RegisterView(FormView):
    success_url = '/'
    url = '/auth/register/'
    template_name = 'loginsys/register.html'


    def get(self, request, context=None):
        context = {'register_form': UserForm()}
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        return self.get(request)


    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return redirect(self.success_url)

        return super(RegisterView, self).dispatch(request, *args, **kwargs)
'''


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
            if user.is_active():
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
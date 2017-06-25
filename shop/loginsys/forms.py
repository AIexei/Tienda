from django.forms import *
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'password')


    email = EmailField(widget=EmailInput(attrs={
                    'class': 'form-control font-mid',
                    'placeholder': 'Email address',
                    'autocomplete': 'off'
                }), required=True, help_text=None)

    first_name = CharField(widget=TextInput(attrs={
                    'class': 'form-control font-mid input-mid',
                    'placeholder': 'Your name',
                    'autocomplete': 'off'
                }), required=True, help_text=None)

    password = CharField(widget=PasswordInput(attrs={
                    'class': 'form-control font-mid input-mid',
                    'placeholder': 'Password',
                    'autocomplete': 'off'
                }), required=True)

    confirm_password = CharField(widget=PasswordInput(attrs={
                    'class': 'form-control font-mid input-last',
                    'placeholder': 'Confirm password',
                    'autocomplete': 'off'
                }), required=True)
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Perfil

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, requiered=True)
    last_name = forms.CharField(max_length=35, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
        model = Perfil
        fields = (
            'celular',
        )



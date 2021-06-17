from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class ProfileForm(UserCreationForm):

    #password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=20, required=True)
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
        help_texts = {k: "" for k in fields} # ayuda a quitar los mensajes de ayuda


class DataProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'chat_id',
        )


class LoginForm(AuthenticationForm):


    def __init__(self, *args, **kwargs):  # es el metodo que ejecuta toda clase de python lo redifinimos
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'






class tokenForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['token']
        labels = {
            'token': 'Ingresar Token: ',
        }
        widgets = {
            'token': forms.PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su token',
                    'name': 'fname',
                    'id': 'token',
                }
            ),
        }
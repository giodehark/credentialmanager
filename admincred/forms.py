import base64

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from . import utils

class ProfileForm(UserCreationForm):

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
#        help_texts = {k: "" for k in fields} # ayuda a quitar los mensajes de ayuda


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



class CredentialForm(forms.ModelForm):
    # MML verificacion de Contraseña
    pwd = forms.CharField(label='Contraseña maestra', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese de login',
            'id': 'pwd',
            'required': 'required',
        }
    ))
    user_cifrado = forms.CharField(label='usuario de la cuenta', widget=forms.TextInput(
        attrs={
            'placeholder': 'ingrese el usuario de la cuenta',
            'name': 'usuario_cuenta',
            'id': 'user_cifrado',
        }
    ))
    pass_cifrado = forms.CharField(label='contraseña cuenta', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Ingrese su contrasena de cuenta',
            'name': 'passcuenta',
            'id': 'pass_cifrado',
        }
    ))

    class Meta:
        model = Credenciales
        fields = ['cuenta', 'notas']
        labels = {
            'cuenta': 'Nombre de la cuenta',
            #'user_cifradoo': 'Usuario de la cuenta',
            #'pass_cifrado': 'Contrasena de cuenta',
            'notas': 'Notas credenciales',

        }
        widgets = {
            'cuenta': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre del sitio o cuenta',
                    'name': 'cuenta',
                    'id': 'cuenta'

                }
            ),
            'notas': forms.TextInput(
                attrs={
                    'placeholder':' ingrese notas de la credencial',
                    'name': 'notas',
                    'id': 'notas'

                }
            )
        }


class PassmasterForm(AuthenticationForm):
    # MML verificacion de Contraseña
    passmaster = forms.CharField(label='Contraseña maestra', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese Passmaster inicio de sesion de este sistema',
            'id': 'passmaster',
        }
    ))
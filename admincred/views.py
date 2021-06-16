from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import utils
from .forms import ProfileForm, DataProfileForm, LoginForm, tokenForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as do_login, logout as do_logout

# Create your views here.

def index(request):
    return render(request, 'index.html')

def profile_register(request):
    register = False
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST)
        data_form = DataProfileForm(data=request.POST)
        if profile_form.is_valid() and data_form.is_valid():
            user = profile_form.save()
            user.set_password(user.password)
            #print(user.set_password(user.password))
            #user.save()
            profile_form.save()
            datapro = data_form.save(commit=False)
            datapro.user = user
            datapro.save()
            data_form.save(commit=False)
            register = True
        else:
            HttpResponse("<h1> Algo malo sucedio </h1>")
    else:
        profile_form = ProfileForm(data=request.POST)
        data_form = DataProfileForm(data=request.POST)
    return render(request, 'registro.html', {
        'profile_form': profile_form,
        'data_form': data_form,
        'register': register,
    })

def login(request):
    valide_user = False
    if request.method == 'POST':
        nameuser = request.POST.get("username")
        passuser = request.POST.get("password")
        user = authenticate(request=request, username=nameuser, password=passuser)
        print(user)
        if user is not None:
            print("encontro al usuario")
            token = utils.generar_token()
            print(token)
            profiletoken = Profile.objects.get(user=user.id)
            profiletoken.token = token
            print(profiletoken.user.username)
            profiletoken.save()
            utils.mandar_mensajebot(token, profiletoken.chat_id)
            try:
                do_login(request,
                         user)
                # request.session.set_expiry(settings.EXPIRY_TIME)
                return redirect('validar')
            except Exception:
                return render(request, 'login.html', {"form": LoginForm, "errores": "Error al iniciar sesión"})
        else:
            return render(request, 'login.html',
                          {"form": LoginForm, "errores": "Usuario y/o contraseña inválidos.",
                           "valide_user": valide_user,
                           })

    elif request.method == "GET":
        return render(request, "login.html",
                      {"form": LoginForm })


def validar_token(request):
    username = request.user.username
    tokenform = tokenForm()

    if request.method == 'POST':
        token = request.POST.get('token')
        token_bd = Profile.objects.get(token=token)
        if token_bd.user.username == username:
            return redirect('menu')
        else:
            return redirect('validar')
    else:
        return render(request, "validar.html",
                      {"form": tokenForm})



def logout(request):
    """Se cerrara sesión ademas de que se borraran los datos de la sesión"""
    request.session.flush()
    respuesta = redirect('login')
    return respuesta



def menu(request):
    '''se tomara al usuario que inicio sesion y se mostraran sus credenciales'''
    username = request.user.username
    return render(request, 'menu_user.html', {
        'username': username,
    })






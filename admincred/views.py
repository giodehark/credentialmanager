from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import utils
from .forms import ProfileForm, DataProfileForm, LoginForm, tokenForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as do_login
from . import decorators
# Create your views here.

def index(request):
    return render(request, 'index.html')

def profile_register(request):
    register = False
    prueba= request.user.id
    print(prueba)
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
            ''' Se toma el id del usuario y en la tabla profile cambia en la columna de valido a true'''
            id_user = request.user.id
            valido_bd = Profile.objects.get(user=id_user)
            print(valido_bd.valido)
            # se guardara en la bd ahora a true en valido
            valido_bd.valido = True
            valido_bd.save()
            print('inicio ')
            print(valido_bd.valido)
            return redirect('menu')
        else:
            return redirect('validar')
    else:
        return render(request, "validar.html",
                      {"form": tokenForm})



def logout(request):
    """Se cerrara sesión ademas de que se borraran los datos de la sesión"""
    id_user = request.user.id
    if id_user != None:
        valido_bd = Profile.objects.get(user=id_user)
        print(valido_bd.valido)
        ''' se guardara en la bd ahora a false en valido'''
        valido_bd.valido = False
        valido_bd.save()
        print('se cerro sesion cambia a:')
        print(valido_bd.valido)
        request.session.flush()
        respuesta = redirect('login')
        return respuesta
    return redirect('login')


@decorators.token_no_validado
def menu(request):
    '''se tomara al usuario que inicio sesion y se mostraran sus credenciales'''

    '''falta poner decorador de inicio sesion y si pasa entonces tomamos el id del usuario
    '''

    ''' en el validar token falta que al autenticar token si esta bien 
    entonces se procede a cambiar a true la columna valido, asi se procedera 
    a crear un decorador que podra ser usado en otras vistas '''
    username = request.user.username

    '''
    id_user =request.user.id

    print(id_user)
    valido_bd = Profile.objects.get(user=id_user)
    print(valido_bd.valido)
    #se guardara en la bd ahora a true en valido
    valido_bd.valido = True
    valido_bd.save()
    print(valido_bd.valido)
    #profilevalido = Profile.objects.get(user=username.id)
    #profilevalido.valido = token
    #print(profilevalido.user.username)
    #profilevalido.save()
    '''

    return render(request, 'menu_user.html', {
        'username': username,
    })






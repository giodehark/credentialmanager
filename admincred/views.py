import base64
from threading import Timer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import utils
from .forms import ProfileForm, DataProfileForm, LoginForm, tokenForm, CredentialForm
from .models import Profile, Credenciales, Compartir
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as do_login
from . import decorators
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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
            return redirect('login')
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
            h = Timer(180.0, utils.deleteToken,(profiletoken,))
            h.start()
            utils.mandar_mensajebot(token, profiletoken.chat_id)
            try:
                do_login(request,
                         user)
                # request.session.set_expiry(settings.EXPIRY_TIME)
                return redirect('validar')
            except Exception:
                form = CredentialForm(request.POST)
                errores = 'Error al iniciar sesión , vuelve a intentarlo'
                return render(request, 'login.html', {"form": LoginForm,
                                                      "errores": errores, })
        else:
            errores = "Usuario y/o contraseña inválidos."
            return render(request, 'login.html',
                          {"form": LoginForm,
                           "errores": errores,
                           })

    elif request.method == "GET":
        return render(request, "login.html",
                      {"form": LoginForm })

@login_required
def validar_token(request):
    username = request.user.username
    tokenform = tokenForm()

    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            token_bd = Profile.objects.get(token=token)
            print(token_bd)
        #if token_bd != None:
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
        except Exception:
            request.session.flush()
            return redirect('login')
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

    username = request.user.username
    return render(request, 'cuentas/menu_user.html', {
        'username': username,
    })

class CrearCredencial(CreateView):
    model = Credenciales
    form_class = CredentialForm
    template_name = 'cuentas/crear_cuenta.html'
    success_url = 'menu'

    def post(self, request, *args, **kwargs):
        passmaster = request.POST['pwd']
        username = request.user.username
        user = User.objects.get(username=username)
        contrasenahash= make_password(passmaster)
        print('verificacion pass')
        print(user.password)
        print(contrasenahash)
        if not check_password(passmaster, user.password):
            form = CredentialForm(request.POST)
            errores= 'Tu contraseña maestra es erronea, vuelve a intentarlo'
            context = {'errores': errores,
                       'form': form,
                       }
            print('No se guardo la credencial passmaster mal')
            return render(request, 'cuentas/crear_cuenta.html', context)
        else:
            form = CredentialForm(request.POST)
            print('entro pass valida')
            if form.is_valid():
                credential=form.save(commit=False)
                credential.user = user
                iv = utils.generarIv()
                llave_aes = utils.generar_llave_aes_from_password(passmaster)
                print('password plana cuenta', request.POST['pass_cifrado'])
                pwd_binario = (request.POST['pass_cifrado']).encode('ascii')
                print('la password binaria', pwd_binario)
                pwd_cifrada = utils.cifrarDatos(pwd_binario, iv, llave_aes)
                print(pwd_cifrada)
                print('usuario no cifrado', request.POST['user_cifrado'])
                user_binario = (request.POST['user_cifrado']).encode('ascii')
                print(('usuario en binario', user_binario))
                user_cifrada = utils.cifrarDatos(user_binario, iv, llave_aes)
                print('usuario cifrado', user_cifrada)
                user_notas = request.POST['notas']
                print('notas guardadas', user_notas)
                credential.pass_cifrado = pwd_cifrada
                credential.user_cifrado = user_cifrada
                iv_plano = base64.b64encode(iv)
                print('iv plano', iv_plano)
                credential.iv = iv_plano
                credential.notas = user_notas
                print('antes del save')
                form.save()
                print('se guardo')
                return redirect('menu')
            else:
                print('no valido el form')
                print(form.errors)

class ListarCredenciales(ListView):
    pass



class EditarCredenciales(UpdateView):
    pass





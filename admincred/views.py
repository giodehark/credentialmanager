from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import utils
from .forms import ProfileForm, DataProfileForm, LoginForm
from .models import Profile
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
            user.save()
            profile = data_form.save(commit=False)
            profile.user = user
            profile.save()
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
        if user is not None:
            valide_user = True
            #SendToken(nameuser)
            try:
                do_login(request,
                         user)  # MML guarda el id del usuario en la sesion almacenado en {{ user }} y aqui se accede como request.session.get("user")
                # request.session.set_expiry(settings.EXPIRY_TIME)
                return redirect('login')
            except Exception:
                return render(request, 'login.html', {"form": LoginForm, "errores": "Error al iniciar sesión"})
        else:
            return render(request, 'login.html',
                          {"form": LoginForm, "errores": "Usuario y/o contraseña inválidos.",
                           "valide_user": valide_user,
                           })

    elif request.method == "GET":
        ip = utils.get_client_ip(request)
        return render(request, "login.html",
                      {"form": LoginForm,
                       "valide_user": valide_user,
                       "ip": ip,
                       })


def logout(request):
    """Se cerrara sesión ademas de que se borraran los datos de la sesión"""
    request.session.flush()
    respuesta = redirect('login')
    return respuesta

def SendToken(nameuser):
    u = User.objects.get(username=nameuser)
    user=nameuser
    u_id = u.id # este es el id del usuario
    #pe = Profile.objects.all()
    #token = Profile.objects.get(user=user.)
    print(u)
    print(u_id)
    #print(token)
    #model = User
    #id_user = User.objects.get(id=pk,username=nameuser)

   # print(id_user)
    #model =Profile
    #token=Profile.objects.






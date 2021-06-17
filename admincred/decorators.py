from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from .models import Profile
from django.contrib.auth.models import User


def token_no_validado(vista):
    def interna(request, pk=""):
        if request.user.is_authenticated:
            id_user = request.user.id
            valido_bd = Profile.objects.get(user=id_user)
            if valido_bd.valido == False:
                print('no paso el token')
                request.session.flush()
                return redirect('login')

            print('si paso el token')
            return vista(request)
        return redirect('login')
    return interna

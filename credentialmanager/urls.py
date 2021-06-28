"""credentialmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from admincred import views
from django.contrib.auth.views import LoginView, LogoutView
from admincred.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registro/', views.profile_register, name='reg'),
    path('accounts/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('validar/', views.validar_token, name='validar'),
    path('user/menu/', views.menu, name='menu'),
    path('user/crear/', login_required(CrearCredencial.as_view(), login_url='login'), name='crear'),
    #path('user/crear/', CrearCredencial.as_view(), name='crear'),
    path('user/listar/', views.CredencialesList, name='listar'),
    path('user/<int:id>/', CredencialDetailView, name='cuenta_detail'),
    path('user/<int:id>/delete/', CredencialDelete, name='eliminar'),
    path('user/<int:id>/editar/', CredencialUpdate, name='actualizar'),
    #path('user/detalles/', CredencialDetailView.as_view(), name='cuenta_detail')
    # path('user/listar/', CredencialesLisView.as_view(template_name="../templates/cuentas/cuentas_list.html"), name='listar'),


]

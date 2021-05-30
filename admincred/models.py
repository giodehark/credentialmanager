from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
#prueba

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=10, blank=False)
    tokenUser = models.CharField(max_length=8, blank=False)
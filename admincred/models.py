from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
#prueba
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=70)
    chat_id = models.CharField(max_length=15)
    valido = models.BooleanField("valido_token", default=False)


    def __str__(self):
        return self.user.username



'''
class Credenciales(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    cuenta = models.CharField("Nombre de cuenta de credencial", max_length=25, blank=False, null=False)
    iv = models.CharField("Vector de inicialización", max_length=70)
    data_cifrada = models.CharField(max_length=70)
    
    
'''
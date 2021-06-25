from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # es usado para general urls por reverse

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=70)
    chat_id = models.CharField(max_length=15)
    valido = models.BooleanField("valido_token", default=False)


    def __str__(self):
        return self.user.username




class Credenciales(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    cuenta = models.CharField("Nombre de cuenta de credencial", max_length=30, blank=False, null=False)
    iv = models.BinaryField("Vector de inicialización", max_length=16, blank=True, null=True)
    user_cifrado = models.CharField(max_length=100, blank=True, null=True)
    pass_cifrado = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(max_length=150, blank=True, null=True)
    user_cifradoo = models.BinaryField(max_length=100, blank=True, null=True)
    pass_cifradoo = models.BinaryField(max_length=100, blank=True, null=True)


    def get_absolute_url(self):
        '''Devuelve el Url de la instancia particular de la credencial'''
        return reverse('cuenta_detail', kwargs={'id': self.id})

    def __str__(self):
        """ El string representara el objeto del modelo """
        return '%s, %s' % (self.user, self.cuenta)


class Compartir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contrasena = models.ForeignKey(Credenciales, on_delete=models.CASCADE)

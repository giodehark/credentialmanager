from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
#prueba
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=70)
    chat_id = models.CharField(max_length=15)


    def __str__(self):
        return self.user.username
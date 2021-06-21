from django.contrib import admin
from .models import Profile, Credenciales
# Register your models here.
admin.site.register(Profile)
admin.site.register(Credenciales)

#class ProfileInline(admin.StackedInline):
 #   model = Profile
  #  verbose_name = "profile"
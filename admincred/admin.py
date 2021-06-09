from django.contrib import admin
from .models import Profile
# Register your models here.
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name = "profile"
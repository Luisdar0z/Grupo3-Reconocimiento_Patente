from django.contrib import admin

from django.contrib.auth.models import Permission
from django.contrib import admin
admin.site.register(Permission)

from django.contrib.auth.models import User

# Definicion de claves por si se olvidan
u = User.objects.get(username__exact = "conserje")
u.set_password("asd123asd123")
u.save()

u = User.objects.get(username__exact = "administrador")
u.set_password("asd123asd123")
u.save()

u = User.objects.get(username__exact = "servidor")
u.set_password("Secret.123")
u.save()

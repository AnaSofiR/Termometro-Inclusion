from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from BiasGuard1.models import *
from django.contrib.auth.models import User, auth
from BiasGuard1.views import *


def loginEmpleo(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        contraseña = request.POST.get('password')
        user = authenticate(username=usuario , password=contraseña)
        if user is not None:
            auth.login(request, user)
            return redirect('empleo')
        else:
            messages.info(request, 'Usuario o contraseña son incorrectos')
            return redirect('loginEmpleo')
        
    return render(request, 'loginEmpleo.html')

def loginEmpresa(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username , password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('inicioEmpresa')
        else:
            messages.info(request, 'Usuario o contraseña son incorrectos')
            return redirect('loginEmpresa')
        
    return render(request, 'loginEmpresa.html')

def inicio(request):
    return render(request, 'inicio.html')
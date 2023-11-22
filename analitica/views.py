from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from .forms import *
from BiasGuard1.models import *
from django.contrib.auth.models import User, auth
from BiasGuard1.views import *
from django.http import HttpResponse, HttpRequest


def loginEmpleo(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        contraseña = request.POST.get('password')
        user = authenticate(username=usuario , password=contraseña)
        if user is not None:
            auth.login(request, user)
            return redirect('inicioEmpleo')
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
            user_id = user.id
            print(user_id)
            return redirect('inicioEmpresa')
        else:
            messages.info(request, 'Usuario o contraseña son incorrectos')
            return redirect('loginEmpresa')
        
    return render(request, 'loginEmpresa.html')

def inicio(request):
    return render(request, 'inicio.html')


def inicioEmpleo(request):
    return render(request, 'inicioEmpleo.html')

def ofertaRating(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    rating = Rating.objects.filter(offer=offer, candidate=request.user.candidates).first()
    offer.candidate_rating = rating.rating if rating else 0
    return render(request, 'ofertaRating.html', {'offer': offer})

def rating(request: HttpRequest, offer_id: int, rating: int) -> HttpResponse:
    offer = Offer.objects.get(id=offer_id)
    Rating.objects.filter(offer=offer, candidate=request.user.candidates).delete()
    offer.rating_set.create(candidate=request.user.candidates, rating=rating)
    return ofertaRating(request, offer_id)

def empleos(request):
    offers = Offer.objects.filter()

    return render(request, 'inicioEmpleo.html', {'offers': offers})
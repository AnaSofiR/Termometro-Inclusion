from django.shortcuts import render, redirect
from django.http import HttpResponse
from .machineLearning import *
from .forms import *
from .models import Offer
import ast
import openai

# Create your views here.

def oferta(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            id_empresa = request.user.companies.id
            offer.company = Companies.objects.get(pk=id_empresa)
            offer.save()
            id = offer.id
            discriminacion_type, palabras_genero, palabras_edad = analizar(id)
            if len(discriminacion_type) == 0:
                return redirect('revision', id_empresa)           
            return redirect('editar',id,palabras_genero, palabras_edad)   
    else:
        form = OfferForm()
    return render(request, 'oferta.html', {'form': form})

def analizar(id_offer):
    oferta = Offer.objects.get(pk=id_offer)
    descripcion = oferta.description
    discrimination_type = []

    #genero,palabras_genero = discriminacionGenero(descripcion)
    edad, palabras_edad = discriminacionEdad(descripcion)
    genero, palabras_genero = discriminacionGenero(descripcion)

    if genero == False:
        oferta.discrimination.add(Discrimination.objects.get(pk=1))
        discrimination_type.append('1')
    if edad == False:
        oferta.discrimination.add(Discrimination.objects.get(pk=2))
        discrimination_type.append('2')
    return discrimination_type, palabras_genero, palabras_edad       
            


#def editar(request, id_offer, discrimination ,palabras_genero,palabras_edad,palabras_discapacidad):

def editar(request, id_offer,palabras_genero,palabras_edad):
    oferta = Offer.objects.get(pk=id_offer)
    descripcion = oferta.description
    descripcion_arr = descripcion.split()
    palabras_genero_list = ast.literal_eval(palabras_genero)
    palabras_edad_list = ast.literal_eval(palabras_edad)
    porcentajeGenero = int((len(palabras_genero_list)*300)/len(descripcion_arr))
    porcentajeEdad = int((len(palabras_edad_list)*300)/len(descripcion_arr))
    sugerencia = "Te sugerio tuki"
 
    context = {
        'offer': oferta,
        'genero': palabras_genero_list,
        'edad': palabras_edad_list,  
        'porcentaje_genero': porcentajeGenero,
        'porcentaje_edad': porcentajeEdad,  
        'sugerencia': sugerencia,
    }

    return render(request, 'editar.html', context)

def inicioEmpresa(request):
    return render(request, 'inicioEmpresa.html')

def empleos(request):
    return render(request, 'empleos.html')

def revision(request, id_empresa):
    empresa = id_empresa
    offers = Offer.objects.filter(company = empresa)

    return render(request, 'revision.html', {'offers': offers})

def publicadas(request):
    return render(request, 'publicadas.html')



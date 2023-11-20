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
            offer.save()
            id = offer.id
            discriminacion_type, palabras_genero, palabras_edad = analizar(id)
            if len(discriminacion_type) == 0:
                return redirect('revision')           
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
    palabras_genero_list = ast.literal_eval(palabras_genero)
    palabras_edad_list = ast.literal_eval(palabras_edad)


    
    '''
    recomendation = discrimination.recomendation
    recomendation_text = recomendation.description
    offer_description = offer.description
    for palabra in palabras_genero:
        offer_description = offer_description.replace(palabra, f'<span style="text-decoration: underline; color: #fdfd96;">{palabra}</span>')

    for palabra in palabras_edad:
        offer_description = offer_description.replace(palabra, f'<span style="text-decoration: underline; color: #03bb85;">{palabra}</span>')

    for palabra in palabras_discapacidad:
        offer_description = offer_description.replace(palabra, f'<span style="text-decoration: underline; color: #a349a4 ;">{palabra}</span>')        

    modified_offer = offer.objects.create(
        title = offer.title,  
        description = offer_description,
        salary = offer.salary, 
        education_level = offer.education_level,
        city = offer.city
    )

    context = {
        'offer': modified_offer,
        'recomendation': recomendation_text
    }

'''    
    context = {
        'offer': oferta,
        'genero': palabras_genero_list,
        'edad': palabras_edad_list,    
    }

    return render(request, 'editar.html', context)

def inicioEmpresa(request):
    return render(request, 'inicioEmpresa.html')

def empleos(request):
    return render(request, 'empleos.html')

def revision(request):
    offers = Offer.objects.filter()

    return render(request, 'revision.html', {'offers': offers})

def publicadas(request):
    return render(request, 'publicadas.html')



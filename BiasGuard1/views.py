from django.shortcuts import render, redirect
from django.http import HttpResponse
from .machineLearning import *
from .forms import *
from .models import Offer
import ast
import openai

# Create your views here.
'''def home(request):
    #return HttpResponse('<h1>Hola</h1>')
    return render(request, 'home.html')
'''    
def revision(request):
    offers = Offer.objects.filter()

    return render(request, 'revision.html', {'offers': offers})


def oferta(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.save()
            id = offer.id
            discriminacion_type, palabras_genero, palabras_edad, palabras_discapacidad = analizar(id)
            if len(discriminacion_type) == 0:
                return redirect('revision')           
            return redirect('editar',id,palabras_genero, palabras_edad, palabras_discapacidad)   
    else:
        form = OfferForm()
    return render(request, 'oferta.html', {'form': form})

def analizar(id_offer):
    oferta = Offer.objects.get(pk=id_offer)
    discrimination_type = []
    palabras_genero = ['mujer','hombre','masculino','femenino','p']
    palabras_edad = ['joven']
    palabras_discapacidad = ['discapacidad']
    genero = False
    edad = False
    discapacidad = False
    '''
    vector = vectorizacionDescripcion(id)
    
    genero, palabras_genero = genero(vector)
    edad, palabras_edad = edad(vector)
    discapacidad, palabras_discapacidad = discapacidad(vector)
    '''

    if genero == False:
        oferta.discrimination.add(Discrimination.objects.get(pk=1))
        discrimination_type.append('1')
    if edad == False:
        oferta.discrimination.add(Discrimination.objects.get(pk=2))
        discrimination_type.append('2')
    if discapacidad == False:
        oferta.discrimination.add(Discrimination.objects.get(pk=3))
        discrimination_type.append('3') 
    return discrimination_type, palabras_genero, palabras_edad, palabras_discapacidad        
            


'''
def editar(request, id_offer, discrimination ,palabras_genero,palabras_edad,palabras_discapacidad):
'''
def editar(request, id_offer,palabras_genero,palabras_edad,palabras_discapacidad):
    oferta = Offer.objects.get(pk=id_offer)
    palabras_genero_list = ast.literal_eval(palabras_genero)
    palabras_edad_list = ast.literal_eval(palabras_edad)
    palabras_discapacidad_list = ast.literal_eval(palabras_discapacidad)


    
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
        'discapacidad': palabras_discapacidad_list
        
    }

    return render(request, 'editar.html', context)

def inicioEmpresa(request):
    return render(request, 'inicioEmpresa.html')

def empleos(request):
    return render(request, 'empleos.html')



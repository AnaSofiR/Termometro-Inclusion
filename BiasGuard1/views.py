from django.shortcuts import render, redirect
from django.http import HttpResponse
from .machineLearning import *
from .forms import *
from .models import Offer
from dotenv import load_dotenv, find_dotenv
import ast
import openai
import os

# Create your views here.

def oferta(request): #Creación de la oferta
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            id_empresa = request.user.companies.id
            offer.company = Companies.objects.get(pk=id_empresa)
            offer.save()
            id = offer.id
            discriminacion_type, palabras_genero, palabras_edad, sugerencia = analizar(id)
            if len(discriminacion_type) == 0:
                return redirect('revision', id_empresa)           
            return redirect('editar',id,palabras_genero, palabras_edad,sugerencia)   
    else:
        form = OfferForm()
    return render(request, 'oferta.html', {'form': form})

def analizar(id_offer): #Análisis de la oferta a través de los modelos SVM
    oferta = Offer.objects.get(pk=id_offer)
    descripcion = oferta.description
    discrimination_type = []
    procesador = ProcesadorLenguajeNatural()
    modelo_genero = ModeloSVMGenero(procesador)
    modelo_edad = ModeloSVMEdad(procesador)

    
    '''
    _ = load_dotenv('modeloSVM/openAi.env')
    openai.api_key  = os.environ['openAI_api_key']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {
                "role": "system", "content": "Eres una maquina analista de ofertas laborales, que se basa en el analisis del discurso. Solamente detectas dos tipos de discriminación: de Género y de Edad. Siempre das una respuesta, exacta y precisa. Debes crear una redacción completa de la oferta eliminando el sesgo, si es que existe alguna oración con sesgo, si todo esta sin sesgo, devuelves la oferta tal cual ingreso. Eres muy inclusivo en todos los sentidos, te gusta incluir a todas las personas."
            },
            {
                "role": "user", "content": f"Genera un analisis de la siguiente oferta:{descripcion}, detectando si existen sesgos de género y/o edad, y dame como respuesta una redacción completa de la oferta eliminando esos tipos de sesgos, si es que existen oraciones con sesgos, si todo está sin sesgos, devuelve la oferta tal cual como ingreso"
            }
        ]
    )

    result = completion.choices[0].message["content"]
    '''
    result = 'Hola'

    edad, palabras_edad = modelo_genero.discriminacionGenero(descripcion)
    genero, palabras_genero = modelo_edad.discriminacionEdad(descripcion)

    if genero == False:
        oferta.discrimination.add(Discrimination.objects.get(pk=1))
        discrimination_type.append('1')
    if edad == False:
        oferta.discrimination.add(Discrimination.objects.get(pk=2))
        discrimination_type.append('2')
    return discrimination_type, palabras_genero, palabras_edad, result       
            


def editar(request, id_offer,palabras_genero,palabras_edad, sugerencia): #Vista para editar la oferta en caso de encontrar algún tipo de discriminación
    oferta = Offer.objects.get(pk=id_offer)
    if request.method == 'POST':
        nueva_descripcion = request.POST.get('descripcion_sugerencia')

        oferta.description = nueva_descripcion
        oferta.save()
        id_empresa = request.user.companies.id

        return redirect('revision', id_empresa)
    
    _ = load_dotenv('modeloSVM/openAi.env')
    openai.api_key  = os.environ['openAI_api_key']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {
                "role": "system", "content": "Eres una maquina analista de ofertas laborales, que se basa en el analisis del discurso. Unicamente detectas racismo y discriminación de edad, no otros sesgos. Siempre das una respuesta, exacta y precisa. Respondes con una redacción completa de la oferta eliminando el sesgo, si es que existe alguna oración con sesgo, si todo esta sin sesgo, devuelves la oferta tal cual ingreso. Eres muy inclusivo en todos los sentidos, te gusta incluir a todas las personas."
            },
            {
                "role": "user", "content": f"Genera un analisis de la siguiente oferta:{oferta.description} y dame como respuesta una redacción completa de la oferta, corrigiendo y eliminando los sesgos de género y edad que encuentres. Dame solamente la redacción de la oferta."
            }
        ]
    )

    result = completion.choices[0].message["content"]


    
    descripcion = oferta.description
    descripcion_arr = descripcion.split()
    palabras_genero_list = ast.literal_eval(palabras_genero)
    palabras_edad_list = ast.literal_eval(palabras_edad)
    porcentajeGenero = int((len(palabras_genero_list)*300)/len(descripcion_arr))
    print(porcentajeGenero)
    porcentajeEdad = int((len(palabras_edad_list)*300)/len(descripcion_arr))
    print(porcentajeEdad)
    sugerenciaOferta = result
 
    context = {
        'offer': oferta,
        'genero': palabras_genero_list,
        'edad': palabras_edad_list,  
        'porcentaje_genero': porcentajeGenero,
        'porcentaje_edad': porcentajeEdad,  
        'sugerencia': sugerenciaOferta,
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

def publicadas(request, id_empresa):
    empresa = id_empresa
    offers = Offer.objects.filter(company = empresa)
    return render(request, 'publicadas.html',{'offers': offers})



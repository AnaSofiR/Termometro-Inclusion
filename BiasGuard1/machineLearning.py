from .views import *
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import string
import re


def buscarDiscriminacion():
 'alguna cosa'




def vectorizacionDescripcion(offer_id):
    offer = offer.objects.get(pk=offer_id)
    offer_description = {offer.description}
    offer_description = genera_caracteristicas(offer_description)


def procesa_oferta(oferta):
    '''
    Limpiamos la oferta con información importante para entrenar los modelos
        input: oferta
        output: oferta limpia
    '''
    stopwords_spanish = stopwords.words('spanish')
    #Elimina puntuación
    oferta = re.sub(r'[^\w\s]', '', oferta)
    # tokenize oferta
    tokenizer = TweetTokenizer(preserve_case=False)
    oferta_tokens = tokenizer.tokenize(oferta)

    oferta_clean = []

    for word in oferta_tokens:
        if word not in stopwords_spanish and word not in string.punctuation:
            oferta_clean.append(word)

    return oferta_clean

def genera_caracteristicas(oferta, freqs):
    '''
    Input:
        oferta: descripción de la oferta
        freqs: diccionario de frecuencias
    Output:
        x: a feature vector of dimension (1,3)
    '''
    # Procesamos los tweets
    word_l = procesa_oferta(oferta)

    # una lista con 2 elementos
    x = [0, 0]

    # Para cada palabra en la lista de palabras tokenizadas
    for word in word_l:
        # El primer componente es la suma de las veces que aparece esa palabra en ofertas adecuadas
        x[0] += freqs.get((word, 1), 0)

        # El segundo componente es la suma de las veces que aparece esa palabra en ofertas discriminatorias
        x[1] += freqs.get((word, 0), 0)
    return x

def genero(description):
    texto_ofensivo = 'modelo_svm.predict([description])'
    palabras_discriminatorias = ['hombre','mujer','femenino','femenina','masculino','masculina','enfermera','limpiadora']
    palabras_encontradas = []
    if texto_ofensivo[0]==False:
        oferta = oferta.lower()
        palabras_texto = oferta.split()
        for palabra in palabras_discriminatorias:
            # Verificar si la palabra está en el texto
            if palabra in palabras_texto:
                palabras_encontradas.append(palabra)

    return bool(texto_ofensivo[0]) , palabras_encontradas


    
def edad(description):
    texto_ofensivo = 'modelo_svm.predict([description])'
    palabras_discriminatorias = ['hombre','mujer','femenino','femenina','masculino','masculina','enfermera','limpiadora']
    palabras_encontradas = []
    if texto_ofensivo[0]==False:
        oferta = oferta.lower()
        palabras_texto = oferta.split()
        for palabra in palabras_discriminatorias:
            # Verificar si la palabra está en el texto
            if palabra in palabras_texto:
                palabras_encontradas.append(palabra)

    return bool(texto_ofensivo[0]) , palabras_encontradas


def discapacidad(description):
    texto_ofensivo = 'modelo_svm.predict([description])'
    palabras_discriminatorias = ['hombre','mujer','femenino','femenina','masculino','masculina','enfermera','limpiadora']
    palabras_encontradas = []
    if texto_ofensivo[0]==False:
        oferta = oferta.lower()
        palabras_texto = oferta.split()
        for palabra in palabras_discriminatorias:
            # Verificar si la palabra está en el texto
            if palabra in palabras_texto:
                palabras_encontradas.append(palabra)

    return bool(texto_ofensivo[0]) , palabras_encontradas
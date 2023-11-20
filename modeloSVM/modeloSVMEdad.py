# -- MANEJO DE LENGUAJE NATURAL --
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import string
import re
nltk.download('stopwords')

import numpy as np

# -- BIBLIOTECAS RELACIONADAS CON SVM
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib


# Abriendo archivos txt con los datos de entrenamiento y test y guardandolos en arreglos
with open('modeloSVM/datosOfertas.txt', 'r') as file:
  ofertas_adecuadas = [linea.strip() for linea in file]

with open('modeloSVM/datosEdad.txt', 'r') as file:
  ofertas_discriminatorias = [linea.strip() for linea in file]

# Dividiendo la lista de datos en entrenamiento y test
train_ofertas_adecuadas = ofertas_adecuadas[:int(len(ofertas_adecuadas) * 0.8)]
train_ofertas_discriminatorias = ofertas_discriminatorias[:int(len(ofertas_adecuadas) * 0.8)]

test_ofertas_adecuadas = ofertas_adecuadas[int(len(ofertas_adecuadas) * 0.8):]
test_ofertas_discriminatorias = ofertas_discriminatorias[int(len(ofertas_adecuadas) * 0.8):]


# Juntando los textos y generando una target
train_ofertas = train_ofertas_adecuadas + train_ofertas_discriminatorias
train_target = [1] * len(train_ofertas_adecuadas) + [0] * len(train_ofertas_discriminatorias)

test_ofertas = test_ofertas_adecuadas + test_ofertas_discriminatorias
test_target = [1] * len(test_ofertas_adecuadas) + [0] * len(test_ofertas_discriminatorias)


#Limpiar textos
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


# Generamos la lista de frecuencias
def genera_frecuencias(lista_ofertas, lista_target):
    ''' Generamos un diccionario con la cantidad de casos positivos
        y negativos para cada palabra
    '''

    frecuencias = {}
    # Recorremos cada par oferta - target
    for oferta, target in zip(lista_ofertas, lista_target):
        # Tokenizamos la oferta
        for word in procesa_oferta(oferta=oferta):
            # Generamos el par (palabra, target)
            par = (word, target)
            # Actualizamos el diccionario de frecuencias
            if par in frecuencias:
                frecuencias[par] += 1
            else:
                frecuencias[par] = 1
    return frecuencias

# Creamos el diccionario de frecuencias
frecuencias = genera_frecuencias(lista_ofertas=train_ofertas, lista_target=train_target)


# Aquí se vectorizan cada uno de los textos
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


# Generando la lista con las ofertas adecuadas y discriminatorias ya vectorizadas
X_train_list = [genera_caracteristicas(x, freqs=frecuencias) for x in train_ofertas]

X_test_list = [genera_caracteristicas(x, freqs=frecuencias) for x in test_ofertas]


# Convirtiendo en matriz
X_train = np.array(X_train_list)
X_test = np.array(X_test_list)
# Generando la target
train_target = np.array(train_target)
test_target = np.array(test_target)

#Creación del modelo machine learning
modelo_svm = SVC(kernel='linear')

#Entrenamiento del modelo
modelo_svm.fit(X_train, np.array(train_target))

# Prediciendo en el conjunto de test
pred_test = modelo_svm.predict(X_test)
precision = accuracy_score(test_target, pred_test)

# Guardamos nuestro modelo entrenado
joblib.dump(modelo_svm, 'modeloSVM/modeloSVMEdad.pkl')
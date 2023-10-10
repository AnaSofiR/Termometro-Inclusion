from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    #return HttpResponse('<h1>Hola</h1>')
    return render(request, 'home.html')

def ofertaLaboral(request):
    return render(request, 'oferta.html')
 